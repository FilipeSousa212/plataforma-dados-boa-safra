# Dicionário de Dados — Comercial Boa Safra (dados brutos dos sistemas)

Dados sintéticos que reproduzem a saída de cada sistema **no seu formato nativo**,
período **jan/2025 – jun/2026**. O objetivo é o realismo da bagunça: formatos,
encodings e chaves diferentes para a mesma realidade.

## Os quatro sistemas

### 1. ERP (Protheus antigo)
Exportações em **CSV Latin-1 (ISO-8859-1)**, separador `;`, decimal `,`, data `DD/MM/AAAA`,
cabeçalhos em MAIÚSCULAS. Um dos arquivos é **posicional (largura fixa)**.

| Arquivo | Conteúdo | Chave |
|---|---|---|
| `ERP_FATURAMENTO.csv` | Todas as vendas faturadas (todos os canais) | `CODCLI`, `CODPROD` |
| `ERP_CLIENTES.csv` | Cadastro de clientes do ERP | `COD_CLI` (numérico), `CNPJ` (mascarado) |
| `ERP_PRODUTOS.csv` | Cadastro de produtos | `COD_PROD`, `EAN` |
| `ERP_TITULOS.TXT` | Contas a receber (posicional) | ver layout abaixo |

**Layout de `ERP_TITULOS.TXT`** (largura fixa, sem separador):
```
FILIAL(2) NUMNOTA(6) PARCELA(2) COD_CLI(6) EMISSAO(8=ddmmaaaa)
VENCTO(8=ddmmaaaa) VALOR(15=centavos, zero à esquerda) STATUS(1: A=aberto B=baixado)
```
A 1ª linha é um cabeçalho de identificação, não um registro.

### 2. Força de vendas (app) — `forca_vendas.xlsx`
Excel com duas abas, cabeçalhos em Title Case, datas como data do Excel.
- **Pedidos**: só o canal representante. Chave `CLIENTE_ID` no formato `UF-nnnn`
  (numeração PRÓPRIA, diferente do ERP) + `CNPJ` **sem máscara** (só dígitos).
- **Visitas**: atividade dos representantes (muitas sem venda = custo de atendimento).

### 3. E-commerce B2B — `ecommerce_pedidos.csv`
CSV **UTF-8** moderno, separador `,`, decimal `.`, data `AAAA-MM-DD`, cabeçalhos
`snake_case`. Só o canal online. Chave = **e-mail do comprador**; produto por **EAN**.
**Não tem CNPJ** e o `customer_name` é digitado pelo comprador (bagunçado ou vazio).

### 4. Planilhas manuais — `planilhas_operacao.xlsx`
Excel "de compras", três abas, com título solto na 1ª linha e chaves digitadas à mão.
- **Custo_Produto**: custo de compra por produto (chave `Cod Produto`, às vezes vazio → só descrição). ~5% dos produtos nem aparecem.
- **Frete_Cliente**: frete médio por cliente. Chave = **nome digitado à mão** (abreviado, sem acento, com typo). ~12% dos clientes não mapeados.
- **Metas_Comissao**: metas e comissão por representante.

## O quebra-cabeça de reconciliação (o coração do projeto)

O mesmo cliente aparece com **quatro chaves diferentes**:

| Sistema | Como identifica o cliente | Exemplo (mesmo cliente) |
|---|---|---|
| ERP faturamento/cadastro | `COD_CLI` numérico | `000091` |
| Força de vendas | `CLIENTE_ID` = `UF-nnnn` | `MG-1035` |
| E-commerce | e-mail do comprador | `compras@...com.br` |
| Planilha de frete | nome digitado à mão | `Empório Bom Dia` / `Emporio Bom Dia` |

**Chaves para religar tudo:**
- **ERP ↔ App**: `CNPJ` — mas mascarado (`71.285.627/0001-84`) vs só dígitos (`71285627000184`) → normalizar antes.
- **ERP/App ↔ E-commerce**: e-commerce **não tem CNPJ** → match por e-mail/nome (fuzzy); parte dos compradores online são novos (sem correspondência).
- **Produtos ERP ↔ E-commerce**: `EAN`.
- **Produtos ↔ Custos / Clientes ↔ Frete**: código ou **nome digitado** (fuzzy).

## Imperfeições propositais (qualidade de dados)
- ~2% do faturamento com `CODCLI` inexistente no cadastro (cadastro incompleto).
- Razão social (ERP) ≠ nome fantasia (app) para o mesmo CNPJ.
- Custo/frete com furos; nomes à mão com abreviação, perda de acento e typo.
- Custo do produto (necessário para margem) **só existe na planilha manual** — o ERP não tem.

> Dados 100% sintéticos, para fins de projeto e demonstração.
