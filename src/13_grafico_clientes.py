import pandas as pd
import matplotlib.pyplot as plt

cli = pd.read_csv("data/processed/margem_por_cliente.csv", dtype={"cliente_id": str})

# 10 clientes que mais dão prejuízo
piores = cli.sort_values("margem_liquida").head(10).copy()
# rótulo: nome do cliente (ou o código, se não tiver nome no cadastro)
piores["rotulo"] = piores["RAZAO_SOCIAL"].fillna("Cliente " + piores["cliente_id"])

plt.figure(figsize=(11, 6))
plt.barh(piores["rotulo"], piores["margem_liquida"], color="crimson")
plt.title("10 clientes que mais dão prejuízo (margem líquida anual)")
plt.xlabel("R$")
plt.gca().invert_yaxis()          # coloca o pior lá no topo
plt.grid(True, axis="x", alpha=0.3)
plt.tight_layout()

plt.savefig("reports/clientes_deficitarios.png", dpi=120)
print("Gráfico salvo em: reports/clientes_deficitarios.png")