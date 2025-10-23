# train_gbt.py
import os
import mlflow, mlflow.spark
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

def get_spark(app_name: str):
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

def main():
    # Import config from parent directory
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import get_config
    
    config = get_config()
    mlflow.set_tracking_uri(config.mlflow_tracking_uri)

    spark = get_spark("train-gbt")
    df = spark.read.format("delta").load("data/delta/gold")

    # Define features that exist in your Walmart file:
    feat = ["promo","sales_lag_1w","sales_ma_4w","sales_ma_8w"]
    for c in ["Fuel_Price","CPI","Unemployment","Temperature"]:
        if c in df.columns:
            feat.append(c)

    from pyspark.ml.feature import VectorAssembler
    assembler = VectorAssembler(inputCols=feat, outputCol="features")

    ds = assembler.transform(df).select("features", df["sales"].alias("label")).na.drop()

    train, test = ds.randomSplit([0.8,0.2], seed=42)

    with mlflow.start_run(run_name="gbt-regression"):
        gbt = GBTRegressor(featuresCol="features", labelCol="label", maxDepth=6, maxIter=150, stepSize=0.1)
        model = gbt.fit(train)
        pred = model.transform(test)

        rmse = RegressionEvaluator(metricName="rmse", labelCol="label", predictionCol="prediction").evaluate(pred)
        mae  = RegressionEvaluator(metricName="mae",  labelCol="label", predictionCol="prediction").evaluate(pred)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.spark.log_model(model, artifact_path="model", registered_model_name="demand_gbt")

        print(f"Training complete. RMSE={rmse:.3f}, MAE={mae:.3f}")

    spark.stop()

if __name__ == "__main__":
    main()
