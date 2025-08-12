import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1754679476914 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="scrap", transformation_ctx="AWSGlueDataCatalog_node1754679476914")

# Script generated for node Change Schema
ChangeSchema_node1754682290412 = ApplyMapping.apply(frame=AWSGlueDataCatalog_node1754679476914, mappings=[("código", "string", "código", "string"), ("ação", "string", "ação", "string"), ("tipo", "string", "tipo", "string"), ("`qtde. teórica`", "string", "qtde", "string"), ("`part. (%)`", "double", "part", "double"), ("date", "string", "date", "string")], transformation_ctx="ChangeSchema_node1754682290412")

# Script generated for node Aggregate
Aggregate_node1754682413562 = sparkAggregate(glueContext, parentFrame = ChangeSchema_node1754682290412, groups = ["tipo", "date"], aggs = [["código", "count"], ["código", "first"], ["ação", "first"], ["qtde", "first"], ["part", "first"]], transformation_ctx = "Aggregate_node1754682413562")

# Script generated for node Change Schema
ChangeSchema_node1754683451750 = ApplyMapping.apply(frame=Aggregate_node1754682413562, mappings=[("tipo", "string", "tipo_acao", "string"), ("date", "string", "date", "string"), ("`count(código)`", "long", "count_código", "long"), ("`first(código)`", "string", "código", "string"), ("`first(ação)`", "string", "ação", "string"), ("`first(qtde)`", "string", "`qtde. teorica`", "string"), ("`first(part)`", "double", "`part. (%)`", "double")], transformation_ctx="ChangeSchema_node1754683451750")

# Script generated for node SQL Query
SqlQuery3326 = '''
SELECT *,
       DATEDIFF(current_date, TO_DATE(date, 'yyyy-MM-dd')) AS dias_coletado
FROM myDataSource
'''
SQLQuery_node1754683826574 = sparkSqlQuery(glueContext, query = SqlQuery3326, mapping = {"myDataSource":ChangeSchema_node1754683451750}, transformation_ctx = "SQLQuery_node1754683826574")

# Script generated for node Salvar
EvaluateDataQuality().process_rows(frame=SQLQuery_node1754683826574, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1754681034725", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Salvar_node1754684266110 = glueContext.getSink(path="s3://fiap-pos-tech/refined/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["date", "ação"], enableUpdateCatalog=True, transformation_ctx="Salvar_node1754684266110")
Salvar_node1754684266110.setCatalogInfo(catalogDatabase="default",catalogTableName="dados_b3_2")
Salvar_node1754684266110.setFormat("glueparquet", compression="snappy")
Salvar_node1754684266110.writeFrame(SQLQuery_node1754683826574)
job.commit()