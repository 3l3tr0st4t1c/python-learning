def soma_diagonais(matriz):
    n_linhas = len(matriz)

    for linha in matriz:
        if len(linha) != n_linhas:
            print("A matriz não é quadrada, digite uma matriz quadrada!")
            return

    soma_principal = 0
    soma_secundaria = 0


    for i in range(n_linhas):
        soma_principal += matriz[i][i]
        soma_secundaria += matriz[i][-i-1]

    print(f"Soma da diagonal principal: {soma_principal}")
    print(f"Soma da diagonal secundaria: {soma_secundaria}")


if __name__=="__main__":
    linhas = int(input("Digite a quantidade de linhas da matriz: "))
    colunas = int(input("Digite a quantidade de colunas da matriz: "))

    if linhas != colunas:
        print("A matriz não é quadrada! Digite uma matriz quadrada!")
    else:
        matriz = []
        print(f"Digite os elementos da matriz {linhas}x{colunas}: ")
        for i in range(linhas):
            linha = []
            for j in range(colunas):
                val = int(input(f"Elemento [{i}][{j}]:"))
                linha.append(val)
            matriz.append(linha)

        soma_diagonais(matriz)
