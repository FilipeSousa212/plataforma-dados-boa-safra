import pandas as pd

# Lê o arquivo do E-COMMERCE (o mais "moderno" e limpo)
ecommerce = pd.read_csv("data/raw/dados_boasafra/ecommerce_pedidos.csv")

# Mostra as 5 primeiras linhas
print("=== E-COMMERCE ===")
print(ecommerce.head())

# Mostra os nomes das colunas e quantas linhas tem
print("\nColunas:", list(ecommerce.columns))
print("Total de linhas:", len(ecommerce))

# Lê o cadastro do ERP do jeito CERTO (ajustando separador e encoding)
print("\n\n=== ERP CLIENTES (leitura correta) ===")
erp = pd.read_csv(
    "data/raw/dados_boasafra/ERP_CLIENTES.csv",
    sep=";",              # o ERP separa colunas por ponto-e-vírgula
    encoding="latin-1"    # o arquivo está no encoding antigo
)
print(erp.head())
print("\nColunas:", list(erp.columns))