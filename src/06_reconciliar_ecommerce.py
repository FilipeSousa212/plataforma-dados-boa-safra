import pandas as pd

# Cadastro mestre = fonte oficial de clientes
mestre = pd.read_csv("data/interim/clientes_mestre.csv", dtype={"cliente_id": str})
ids_mestre = set(mestre["cliente_id"])

# Compradores únicos do e-commerce (um por e-mail)
ec = pd.read_csv("data/raw/dados_boasafra/ecommerce_pedidos.csv")
compradores = ec[["customer_email", "customer_name"]] \
    .drop_duplicates(subset=["customer_email"]).copy()

# O E-MAIL é a chave estável do e-commerce.
# Extrai a referência ao cliente e formata como código de 6 dígitos.
compradores["cliente_id"] = compradores["customer_email"].str.extract(r"(\d+)")[0].str.zfill(6)

# VALIDAÇÃO: só confio no id se ele existir no cadastro mestre
compradores["valido"] = compradores["cliente_id"].isin(ids_mestre)

print("Compradores no e-commerce:", len(compradores))
print("Ligados a cliente conhecido:", compradores["valido"].sum())
print("Sem correspondência (clientes novos só online):", (~compradores["valido"]).sum())

# Salva a ponte e-mail -> cliente_id (só os válidos) na camada prata
ponte_ec = compradores[compradores["valido"]][["customer_email", "cliente_id"]]
ponte_ec.to_csv("data/interim/ecommerce_clientes.csv", index=False)
print("\nSalvo: data/interim/ecommerce_clientes.csv")