permissoes = [1, 2, 4, 8, 0, 16]

for p in permissoes:
    if p <= 0:
        print("Falha: permissão inválida detectada.")
        break
else:
    print("Sucesso: todas as permissões válidas.")
