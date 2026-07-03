import pandas as pd

# Carrega o cadastro do ERP já limpo. dtype=str evita que o pandas
# "coma os zeros" de novo ao ler o CSV.
erp = pd.read_csv(
    "data/interim/erp_clientes.csv",
    dtype={"CNPJ_LIMPO": str, "COD_CLI": str}
)

# Lê os pedidos do app de força de vendas (Excel, aba "Pedidos")
app = pd.read_excel(
    "data/raw/dados_boasafra/forca_vendas.xlsx",
    sheet_name="Pedidos"
)

# Do app, queremos só a lista de clientes únicos (id, cnpj, nome)
clientes_app = app[["CLIENTE_ID", "CNPJ", "Cliente"]].drop_duplicates()

# Garante que o CNPJ do app seja texto de 14 dígitos (mesmo formato do ERP)
clientes_app["CNPJ_LIMPO"] = clientes_app["CNPJ"].astype(str).str.zfill(14)

print("Clientes únicos no app:", len(clientes_app))

# A COSTURA: liga app -> ERP pelo CNPJ (igual a um PROCV)
ponte = clientes_app.merge(
    erp[["COD_CLI", "RAZAO_SOCIAL", "CNPJ_LIMPO"]],
    on="CNPJ_LIMPO",   # coluna em comum
    how="left"          # mantém todos os clientes do app
)

# Quantos encontraram par no ERP?
casaram = ponte["COD_CLI"].notna().sum()
print(f"Casaram com o ERP: {casaram} de {len(ponte)}")
print(ponte.head(10))

# --- MONTA O CADASTRO MESTRE (uma chave pra reger todas) ---

# Do resultado da costura, pega o mapa: código ERP  <->  id do app
mapa_app = ponte[["COD_CLI", "CLIENTE_ID"]].dropna().drop_duplicates()

# Parte do cadastro do ERP (nossa base oficial) e pendura o id do app
mestre = erp.merge(mapa_app, on="COD_CLI", how="left")

# Elege a CHAVE ÚNICA do projeto: o código do ERP vira "cliente_id"
mestre = mestre.rename(columns={"COD_CLI": "cliente_id"})

# Guarda só o que interessa no cadastro mestre
mestre = mestre[["cliente_id", "RAZAO_SOCIAL", "CNPJ_LIMPO", "UF",
                 "MUNICIPIO", "SEGMENTO", "CLIENTE_ID"]]

print("=== CADASTRO MESTRE ===")
print("Total de clientes:", len(mestre))
print("Com identidade no app:", mestre["CLIENTE_ID"].notna().sum())
print(mestre.head(8).to_string())

mestre.to_csv("data/interim/clientes_mestre.csv", index=False)
print("\nSalvo: data/interim/clientes_mestre.csv")