import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')

    # Nome do job criado no Glue
    job_name = 'fiap-tech'

    # Inicia o job de ETL no Glue
    response = glue.start_job_run(JobName=job_name)

    print(f"Glue job iniciado: {response['JobRunId']}")
    
    return {
        'statusCode': 200,
        'body': f"Glue job iniciado: {response['JobRunId']}"
    }
