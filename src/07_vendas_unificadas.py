import pandas as pd

# Faturamento limpo (prata). O ERP = TODAS as vendas faturadas.
fat = pd.read_csv(
    "data/interim/erp_faturamento.csv",
    dtype={"CODCLI": str}, parse_dates=["EMISSAO"]
)

# --- DESMASCARANDO A SOMA ERRADA ---
app = pd.read_excel("data/raw/dados_boasafra/forca_vendas.xlsx", sheet_name="Pedidos")
ec = pd.read_csv("data/raw/dados_boasafra/ecommerce_pedidos.csv")
ec_total = (ec["qty"] * ec["unit_price"]).sum()

soma_ingenua = fat["VLRTOTAL"].sum() + app["Total"].sum() + ec_total
print("Soma ingênua dos 3 sistemas:  R$ {:>14,.2f}".format(soma_ingenua))
print("Faturamento REAL (só ERP):    R$ {:>14,.2f}".format(fat["VLRTOTAL"].sum()))
print("Ilusão de duplicidade:        R$ {:>14,.2f}".format(soma_ingenua - fat["VLRTOTAL"].sum()))

# --- FONTE ÚNICA DE VENDAS (camada ouro) ---
# a chave única do projeto
vendas = fat.rename(columns={"CODCLI": "cliente_id"})

# enriquece com nome/UF/segmento do cadastro mestre
mestre = pd.read_csv("data/interim/clientes_mestre.csv", dtype={"cliente_id": str})
vendas = vendas.merge(
    mestre[["cliente_id", "RAZAO_SOCIAL", "UF", "SEGMENTO"]],
    on="cliente_id", how="left"
)

vendas.to_csv("data/processed/vendas_unificadas.csv", index=False)
print("\nFonte única de vendas salva em: data/processed/vendas_unificadas.csv")
print("Linhas:", len(vendas), "| Clientes:", vendas["cliente_id"].nunique())