# etl_incremental.py
import os
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip

def get_spark(app_name: str):
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

def main():
    spark = get_spark("retail-etl")

    bronze = "data/delta/bronze"
    silver = "data/delta/silver"
    gold   = "data/delta/gold"

    # Ingest raw CSV(s) -> Bronze
    raw = spark.read.option("header", True).option("inferSchema", True).csv("data/raw/*.csv")
    raw.write.format("delta").mode("append").save(bronze)

    # Bronze -> Silver (basic cleaning/types and schema mapping)
    df = spark.read.format("delta").load(bronze)
    
    # Map Walmart schema -> our canonical names (adjust if your columns differ)
    df = (df
        .withColumnRenamed("Date", "date")
        .withColumnRenamed("Store", "store_id")
        .withColumnRenamed("Weekly_Sales", "sales")
        .withColumnRenamed("Holiday_Flag", "promo")
        .withColumn("date", F.to_date("date", "dd-MM-yyyy"))  # Handle DD-MM-YYYY format
        .dropna(subset=["date","store_id","sales"])
    )
    df.write.format("delta").mode("overwrite").save(silver)

    # Silver -> Gold (weekly features for Walmart data)
    g = spark.read.format("delta").load(silver)
    w = Window.partitionBy("store_id").orderBy("date")  # No item_id in Walmart data
    
    # Build weekly features (lags & moving averages over weeks)
    g = (g
         .withColumn("sales_lag_1w", F.lag("sales", 1).over(w))
         .withColumn("sales_ma_4w", F.avg("sales").over(w.rowsBetween(-3, 0)))
         .withColumn("sales_ma_8w", F.avg("sales").over(w.rowsBetween(-7, 0)))
         .fillna(0, subset=["sales_lag_1w","sales_ma_4w","sales_ma_8w","promo"])
    )
    
    # Keep macro features if present
    for c in ["Fuel_Price","CPI","Unemployment","Temperature"]:
        if c in g.columns:
            g = g.fillna({c: 0})
    
    g.write.format("delta").mode("overwrite").save(gold)

    print("ETL complete. Gold table updated at:", gold)
    spark.stop()

if __name__ == "__main__":
    main()
