from pyathena import connect
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
athena_db = 'default'
athena_table = 'dados_b3_2'
s3_staging_dir = 's3://fiap-pos-tech/athena/'  # pasta onde o Athena salva os resultados

# Conexão com o Athena
conn = connect(
    s3_staging_dir=s3_staging_dir,
    region_name='sa-east-1'  # ajuste se necessário
)

# Consulta SQL
query = f"SELECT * FROM {athena_db}.{athena_table} LIMIT 20"
df = pd.read_sql(query, conn)

# Mostrar primeiras linhas
print(df.head())

# Gráfico de exemplo
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='tipo_acao')
plt.title('Quantidade de Ações por Tipo')
plt.xticks(rotation=45)
plt.show()
plt.show(block=True)
input("Pressione Enter para fechar o gráfico...")