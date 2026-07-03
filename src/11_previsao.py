import pandas as pd

vendas = pd.read_csv("data/processed/vendas_unificadas.csv", parse_dates=["EMISSAO"])
vendas["ano"] = vendas["EMISSAO"].dt.year
vendas["mes_num"] = vendas["EMISSAO"].dt.month
t = vendas.pivot_table(index="mes_num", columns="ano", values="VLRTOTAL", aggfunc="sum")

# 1. Crescimento médio observado (jan-jun têm os dois anos)
crescimento = (t[2026] / t[2025] - 1).dropna().mean()
print(f"Crescimento médio ano a ano: {crescimento*100:.1f}%")

# 2. Prevê jul-dez/2026 = mesmo mês de 2025 x (1 + crescimento)
prev = []
for m in range(7, 13):
    base = t.loc[m, 2025]
    prev.append({
        "mes": f"2026-{m:02d}",
        "base_2025": round(base, 0),
        "previsto_2026": round(base * (1 + crescimento), 0),
    })
prev = pd.DataFrame(prev)

print("\n=== Previsão de faturamento — 2º semestre 2026 ===")
print(prev.to_string(index=False))
print(f"\nTotal previsto jul-dez/2026: R$ {prev['previsto_2026'].sum():,.0f}")

prev.to_csv("data/processed/previsao_vendas.csv", index=False)
print("Salvo: data/processed/previsao_vendas.csv")
