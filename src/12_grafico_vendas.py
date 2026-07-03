import pandas as pd
import matplotlib.pyplot as plt

# Histórico mensal (real)
vendas = pd.read_csv("data/processed/vendas_unificadas.csv", parse_dates=["EMISSAO"])
vendas["mes"] = vendas["EMISSAO"].dt.to_period("M").dt.to_timestamp()
serie = vendas.groupby("mes")["VLRTOTAL"].sum()

# Previsão (jul-dez/2026)
prev = pd.read_csv("data/processed/previsao_vendas.csv")
prev["mes"] = pd.to_datetime(prev["mes"])

# --- desenha o gráfico ---
plt.figure(figsize=(11, 5))
plt.plot(serie.index, serie.values, marker="o", label="Faturamento real")
plt.plot(prev["mes"], prev["previsto_2026"], marker="o", linestyle="--",
         color="orange", label="Previsão")

plt.title("Faturamento mensal — Comercial Boa Safra")
plt.ylabel("R$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# salva a imagem na pasta reports
plt.savefig("reports/faturamento_mensal.png", dpi=120)
print("Gráfico salvo em: reports/faturamento_mensal.png")