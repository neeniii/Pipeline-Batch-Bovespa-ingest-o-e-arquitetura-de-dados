import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import io
from datetime import datetime
from io import StringIO
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Nome do bucket e prefixo
BUCKET_NAME = 'fiap-pos-tech'
PREFIX = 'scrap'

#coletar os dados da B3
def b3_data():

     # Configurações do Chrome em modo headless
    options = Options()
    options.add_argument('--headless')  # sem abrir janela
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Instala automaticamente o ChromeDriver correto
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Acessa o site da B3
    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'
    driver.get(url)

    # Aguarda o carregamento dos dados via JavaScript
    time.sleep(5)

    html = driver.page_source
    driver.quit()

    # Extração com BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')

    if table:
        df = pd.read_html(StringIO(str(table)))[0]
        return df
    else:
        raise Exception("Tabela não encontrada no HTML da B3")

#salvar em parquet e subir para o s3
def save_parquet_s3(df, bucket, prefix):
    today = datetime.today().strftime('%Y-%m-%d')
    partition_path = f"{prefix}/date={today}/dados.parquet"

    table = pa.Table.from_pandas(df)
    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)

    s3 = boto3.client('s3')
    s3.upload_fileobj(buffer, bucket, partition_path)
    print(f"Arquivo enviado para s3://{bucket}/{partition_path}")
#coleta os dados da B3 e envia para o S3
if __name__ == '__main__':
    df = b3_data()
    save_parquet_s3(df, BUCKET_NAME, PREFIX)