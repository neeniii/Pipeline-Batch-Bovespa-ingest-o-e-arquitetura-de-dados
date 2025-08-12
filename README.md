📌 Visão Geral
# Este projeto implementa um pipeline de ingestão e transformação de dados da B3 utilizando os serviços da AWS.
# O objetivo é coleta de dados, armazenamento, processamento, catalogação e consulta no Athena.

🛠 Arquitetura
- Scraping da B3 → Captura os dados de ações e salva no Amazon S3 em formato Parquet, particionado por data.**(local no vs code)**

- Lambda → Dispara automaticamente quando um novo arquivo é adicionado ao bucket e inicia o AWS Glue Job.**(O script foi feito direto no AWS no lambda)**

- AWS Glue (Visual) → Processa os dados, aplica transformações e salva no S3 na pasta refined/, também em formato Parquet, particionado por data e nome da ação.

- Glue Crawler → Atualiza o Glue Catalog para disponibilizar os dados no Athena.

- Athena → Permite consultar e analisar os dados processados.

- Visualização → Gráfico utilizando a biblioteca matplotlib, onde mostrei a quantidade de Ações por Tipo. **(local no vs code)**

# Como rodar localmente (Vs Code)

1. Crie um ambiente virtual:
   
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   

3. Instale as bibliotecas:
   
   pip install -r requirements.txt
   

4. Execute o scrao local:
   
   python lambda/scrap.py
   ```

📂 Estrutura do Projeto

📦 projeto-b3-aws
 ┣ 📂 lambda
 ┃ ┗ lambda_function.py   # Código da função Lambda
 ┣ 📂 glue
 ┃ ┗ glue.py   # Código do script do glue
 ┃  ┗ glue.json   # Código do script do glue
 ┣ 📂 gráfico
 ┃ ┗ grafico.py  # Script visualização dos dados
 ┣ 📂 scrap_b3
 ┃ ┗ 📜 scrap.py  # Script de coleta e upload para o S3
 ┣ 📜 README.md
 ┣ 📜 requirements.txt # arquivo com todas as bibliotecas para instalar.
 ┣ 📜 .gitignore
 
⚙️ Tecnologias Utilizadas
'''
- [boto3](https://pypi.org/project/boto3/)
- [Pandas](https://pandas.pydata.org/)
- [lxml](https://lxml.de/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [pyarrow](https://pypi.org/project/pyarrow/)
- [Requests](https://docs.python-requests.org/)
- [selenium](https://pypi.org/project/selenium/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- [PyAthena](https://pypi.org/project/PyAthena/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [seaborn](https://pypi.org/project/seaborn/)

⚙️ Serviços AWS Utilizados
- Amazon S3 → Armazenamento dos dados brutos e refinados.

- AWS Lambda → Função que aciona o Glue Job automaticamente.

- AWS Glue → Job visual para ETL (extração, transformação e carga).

- AWS Glue Crawler → Atualiza automaticamente o catálogo de dados.

- Amazon Athena → Consulta SQL sobre os dados no S3.

🔐 Permissões IAM
# Foram criadas 2 regras no IAM:

# Regra do Lambda com a política:

- AWSLambdaBasicExecutionRole

# Regra do Glue com as políticas:

- AmazonS3FullAccess

- AWSGlueServiceRole

📜 Lambda Function
# O código da função Lambda não está neste README, mas está localizado na pasta lambda/.

# Função principal da Lambda:

- É acionada automaticamente via evento S3 (PUT).

- Inicia o Glue Job responsável por processar os dados.

🔄 Fluxo do Pipeline
- O script scrap.py coleta os dados da B3 e envia para o bucket S3 na pasta scrap/date=YYYY-MM-DD/.

- O S3 Event Trigger detecta o upload e aciona a Lambda.

- A Lambda chama o Glue Job.

O Glue Job:

- Agrupa, renomeia e realiza cálculo com datas.

- Salva os dados no S3 em refined/date=YYYY-MM-DD/acao=ABC/.

- O Glue Crawler atualiza o catálogo.

- O Athena lê os dados e permite consultas SQL.

📊 Consultando no Athena
- Abra o Amazon Athena.

- No banco de dados configurado pelo Glue Crawler, selecione a tabela de dados refinados.

Execute consultas SQL, por exemplo:

SELECT * 
FROM dados_b3_2
WHERE date = '2025-08-05';

👨‍💻 Autor

Gabriel Pereira Ferreira.