permissoes = [1, 2, 4, 8, 0, 16]
tem_permissao_invalida = False

for i in permissoes:
    if i <= 0:
       tem_permissao_invalida = True
       break

if tem_permissao_invalida == True:
    print("Falha: permissão inválida detectada.")
else:
    print("Sucesso: todas as permissões válidas")
