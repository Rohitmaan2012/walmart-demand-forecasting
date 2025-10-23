# batch_infer.py
import os, sys
import mlflow
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler

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
    horizon = int(sys.argv[1]) if len(sys.argv)>1 else config.prediction_horizon_days
    model_uri = os.environ.get("MODEL_URI", f"models:/{config.model_name}/{config.model_stage}")

    spark = get_spark("batch-infer")
    gold = spark.read.format("delta").load("data/delta/gold")
    latest = gold.agg(F.max("date").alias("maxd")).collect()[0]["maxd"]
    scoring = gold.filter(F.col("date")==latest)

    feat_cols = ["promo","sales_lag_1w","sales_ma_4w","sales_ma_8w"]
    for c in ["Fuel_Price","CPI","Unemployment","Temperature"]:
        if c in scoring.columns:
            feat_cols.append(c)

    from pyspark.ml.feature import VectorAssembler
    scoring = VectorAssembler(inputCols=feat_cols, outputCol="features").transform(scoring)

    try:
        model = mlflow.spark.load_model(model_uri)
    except Exception as e:
        # Fallback to latest run's model if Production stage not set
        print("MODEL_URI load failed, trying local run artifact…", e)
        from mlflow.tracking import MlflowClient
        client = MlflowClient()
        runs = client.search_runs(experiment_ids=["0"], order_by=["attributes.start_time DESC"], max_results=1)
        uri = f"runs:/{runs[0].info.run_id}/model"
        model = mlflow.spark.load_model(uri)

    pred = model.transform(scoring).select("date","store_id",F.col("prediction").alias("forecast_sales"))
    out = f"outputs/predictions/date={latest}"
    pred.write.mode("overwrite").parquet(out)
    print("Predictions written to:", out)
    spark.stop()

if __name__ == "__main__":
    main()
