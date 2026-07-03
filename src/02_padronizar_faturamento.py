import pandas as pd

# Lê o faturamento do ERP (mesmos ajustes: separador e encoding)
fat = pd.read_csv(
    "data/raw/dados_boasafra/ERP_FATURAMENTO.csv",
    sep=";",
    encoding="latin-1"
)

print(fat.head())
print("\nTipos de cada coluna:")
print(fat.dtypes)

# --- LIMPEZA (bronze -> prata) ---

# 1. Colunas de dinheiro: troca vírgula por ponto e vira número
for col in ["VLRUNIT", "VLRTOTAL"]:
    fat[col] = fat[col].str.replace(",", ".").astype(float)

# 2. Data: texto "dd/mm/aaaa" vira data de verdade
fat["EMISSAO"] = pd.to_datetime(fat["EMISSAO"], format="%d/%m/%Y")

# 3. Código do cliente: vira texto com 6 dígitos (devolve os zeros da frente)
fat["CODCLI"] = fat["CODCLI"].astype(str).str.zfill(6)

# Confere se os tipos mudaram
print("\n=== DEPOIS DA LIMPEZA ===")
print(fat.dtypes)
print("\nAgora dá pra somar. Faturamento total do ERP: R$", round(fat["VLRTOTAL"].sum(), 2))

# Salva a versão limpa na camada PRATA (data/interim)
fat.to_csv("data/interim/erp_faturamento.csv", index=False)
print("\nArquivo limpo salvo em: data/interim/erp_faturamento.csv")