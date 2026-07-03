import pandas as pd

vendas = pd.read_csv("data/processed/vendas_unificadas.csv", dtype={"cliente_id": str})
mestre = pd.read_csv("data/interim/clientes_mestre.csv", dtype={"cliente_id": str})
ids = set(mestre["cliente_id"])

# --- 1. Margem bruta (receita - custo do produto) ---
custo = pd.read_excel("data/raw/dados_boasafra/planilhas_operacao.xlsx",
                      sheet_name="Custo_Produto", skiprows=1)
custo = custo.rename(columns={"Cod Produto": "CODPROD", "Custo Compra (R$)": "custo_unit"})
custo["custo_unit"] = custo["custo_unit"].astype(str).str.replace(",", ".").astype(float)
custo = custo[["CODPROD", "custo_unit"]].dropna(subset=["CODPROD"])

v = vendas.merge(custo, on="CODPROD", how="left")
v["margem_bruta"] = v["VLRTOTAL"] - v["QUANT"] * v["custo_unit"]
cli = v.groupby("cliente_id").agg(
    receita=("VLRTOTAL", "sum"),
    margem_bruta=("margem_bruta", "sum"),
).reset_index()

# --- 2. Comissão dos representantes (app), por cliente ---
app = pd.read_excel("data/raw/dados_boasafra/forca_vendas.xlsx", sheet_name="Pedidos")
app["comissao"] = app["Total"] * app["Comissão %"] / 100
mapa = mestre.dropna(subset=["CLIENTE_ID"])[["cliente_id", "CLIENTE_ID"]]
com = app.merge(mapa, on="CLIENTE_ID", how="left").groupby("cliente_id")["comissao"].sum().reset_index()
cli = cli.merge(com, on="cliente_id", how="left")

# --- 3. Frete por cliente (planilha manual) ---
frete = pd.read_excel("data/raw/dados_boasafra/planilhas_operacao.xlsx",
                      sheet_name="Frete_Cliente", skiprows=1)
frete["Frete por Entrega (R$)"] = frete["Frete por Entrega (R$)"].astype(str).str.replace(",", ".").astype(float)
# reaproveita a técnica do e-commerce: extrai o código do nome e valida no cadastro
frete["cliente_id"] = frete["Cliente"].astype(str).str.extract(r"(\d+)")[0].str.zfill(6)
frete["frete_anual"] = frete["Frete por Entrega (R$)"] * frete["Nº Entregas/Mês"] * 12
frete = frete[frete["cliente_id"].isin(ids)][["cliente_id", "frete_anual"]] \
    .groupby("cliente_id").sum().reset_index()
cli = cli.merge(frete, on="cliente_id", how="left")

# --- 4. Margem líquida ---
cli[["comissao", "frete_anual"]] = cli[["comissao", "frete_anual"]].fillna(0)
cli["margem_liquida"] = cli["margem_bruta"] - cli["comissao"] - cli["frete_anual"]

cli = cli.merge(mestre[["cliente_id", "RAZAO_SOCIAL", "SEGMENTO"]], on="cliente_id", how="left")
cli = cli.sort_values("margem_liquida")

deficit = cli[cli["margem_liquida"] < 0]
print(f"Total de clientes: {len(cli)}")
print(f"Clientes deficitários: {len(deficit)} ({len(deficit)/len(cli)*100:.0f}%)")
print(f"Prejuízo somado: R$ {deficit['margem_liquida'].sum():,.0f}")
print("\n=== 8 clientes que mais dão prejuízo ===")
print(deficit.head(8)[["cliente_id","RAZAO_SOCIAL","receita","frete_anual","margem_liquida"]].round(0).to_string(index=False))

cli.to_csv("data/processed/margem_por_cliente.csv", index=False)
print("\nSalvo: data/processed/margem_por_cliente.csv")