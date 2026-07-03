import pandas as pd

# Lê o cadastro de clientes do ERP
cli = pd.read_csv(
    "data/raw/dados_boasafra/ERP_CLIENTES.csv",
    sep=";",
    encoding="latin-1"
)

# 1. COD_CLI: texto com 6 dígitos (mesma regra do faturamento, pra casar depois)
cli["COD_CLI"] = cli["COD_CLI"].astype(str).str.zfill(6)

# 2. CNPJ: cria uma coluna nova só com os números (tira . / -)
cli["CNPJ_LIMPO"] = cli["CNPJ"].str.replace(r"\D", "", regex=True)

print(cli.head())

# Salva na camada prata
cli.to_csv("data/interim/erp_clientes.csv", index=False)
print("\nSalvo: data/interim/erp_clientes.csv")