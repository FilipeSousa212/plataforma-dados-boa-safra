import pandas as pd

# 1. Fonte única de vendas (ouro)
vendas = pd.read_csv("data/processed/vendas_unificadas.csv", dtype={"cliente_id": str})

# 2. Custo dos produtos (planilha manual: 1a linha é título solto -> skiprows=1)
custo = pd.read_excel(
    "data/raw/dados_boasafra/planilhas_operacao.xlsx",
    sheet_name="Custo_Produto", skiprows=1
)
custo = custo.rename(columns={"Cod Produto": "CODPROD", "Custo Compra (R$)": "custo_unit"})
custo["custo_unit"] = custo["custo_unit"].astype(str).str.replace(",", ".").astype(float)
custo = custo[["CODPROD", "custo_unit"]].dropna(subset=["CODPROD"])

# 3. Cola o custo em cada linha de venda (PROCV pelo código do produto)
vendas = vendas.merge(custo, on="CODPROD", how="left")

sem_custo = vendas["custo_unit"].isna().mean() * 100
print(f"Atenção: {sem_custo:.1f}% das linhas estão SEM custo cadastrado (furo da planilha).")

# 4. Custo total e margem bruta por linha
vendas["custo_total"] = vendas["QUANT"] * vendas["custo_unit"]
vendas["margem_bruta"] = vendas["VLRTOTAL"] - vendas["custo_total"]

# 5. Agrupa por cliente (igual a uma tabela dinâmica do Excel)
resumo = vendas.groupby(["cliente_id", "RAZAO_SOCIAL"]).agg(
    receita=("VLRTOTAL", "sum"),
    custo=("custo_total", "sum"),
    margem_bruta=("margem_bruta", "sum"),
).reset_index()
resumo["margem_%"] = (resumo["margem_bruta"] / resumo["receita"] * 100).round(1)

resumo = resumo.sort_values("margem_%")
print("\n=== 8 clientes com PIOR margem bruta (%) ===")
print(resumo.head(8).to_string(index=False))
print("\n=== 5 clientes com MELHOR margem bruta (%) ===")
print(resumo.tail(5).to_string(index=False))