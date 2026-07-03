import pandas as pd

vendas = pd.read_csv("data/processed/vendas_unificadas.csv", parse_dates=["EMISSAO"])

# 1. Série mensal: soma do faturamento por mês
vendas["mes"] = vendas["EMISSAO"].dt.to_period("M")
serie = vendas.groupby("mes")["VLRTOTAL"].sum().round(0)
print("=== Faturamento por mês ===")
print(serie.to_string())

# 2. Enxergar sazonalidade: 2025 x 2026 lado a lado
vendas["ano"] = vendas["EMISSAO"].dt.year
vendas["mes_num"] = vendas["EMISSAO"].dt.month
tabela = vendas.pivot_table(index="mes_num", columns="ano",
                            values="VLRTOTAL", aggfunc="sum").round(0)
tabela["cresc_%"] = ((tabela[2026] / tabela[2025] - 1) * 100).round(1)
print("\n=== 2025 x 2026 por mês (sazonalidade nas linhas, crescimento na coluna) ===")
print(tabela.to_string())