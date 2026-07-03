from rapidfuzz import fuzz

# Compara pares de nomes e dá uma nota de parecença (0 a 100)
print(fuzz.ratio("Merc. Central 196", "Mercado Central 196"))
print(fuzz.ratio("Padaria Estrela 087", "Padaria Estrela 87"))
print(fuzz.ratio("Merc. Central 196", "Bar do Zé 300"))