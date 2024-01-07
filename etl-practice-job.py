import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node1704609631466 = glueContext.create_dynamic_frame.from_catalog(
    database="etl-practice-database",
    table_name="coffee_csv",
    transformation_ctx="AmazonS3_node1704609631466",
)

# Script generated for node Change Schema
ChangeSchema_node1704609748114 = ApplyMapping.apply(
    frame=AmazonS3_node1704609631466,
    mappings=[
        ("order_id", "long", "Order_id", "bigint"),
        ("coffee", "string", "Coffee", "string"),
        ("cust_name", "string", "Cust_name", "string"),
        ("drive_thru", "string", "Drive_thru", "string"),
        ("walk_in", "string", "Walk_in", "string"),
    ],
    transformation_ctx="ChangeSchema_node1704609748114",
)

# Script generated for node Filter
Filter_node1704609836131 = Filter.apply(
    frame=ChangeSchema_node1704609748114,
    f=lambda row: (bool(re.match("Y", row["Walk_in"]))),
    transformation_ctx="Filter_node1704609836131",
)

# Script generated for node Amazon S3
AmazonS3_node1704610004161 = glueContext.write_dynamic_frame.from_options(
    frame=Filter_node1704609836131,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://etl-practice-bucket-vks/output/",
        "compression": "snappy",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1704610004161",
)

job.commit()
