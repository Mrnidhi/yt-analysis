import sys
from pyspark.context import SparkContext
from pyspark.sql.functions import lit, current_date
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="yt_base",
    table_name="clean"
)

# this converts Spark to DataFrame
df = input_dyf.toDF()

df = df.withColumn("region", lit("US"))  # Customize later if needed
df = df.withColumn("trending_date", current_date())

# converts back to Glue DynamicFrame
output_dyf = DynamicFrame.fromDF(df, glueContext, "output_dyf")

glueContext.write_dynamic_frame.from_options(
    frame=output_dyf,
    connection_type="s3",
    connection_options={
        "path": "s3://youtube-trend-nidhi/youtube-trending-datalake/analytics/",
        "partitionKeys": ["region", "trending_date"]
    },
    format="parquet"
)

job.commit()
