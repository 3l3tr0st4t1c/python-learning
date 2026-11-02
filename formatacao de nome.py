def formatar_nome(nome_completo: str) -> str:
    particulas = {"DE", "DA", "DO", "DAS", "DOS", "E"}

    palavras = nome_completo.strip().upper().split()

    if not palavras:
        return ""

    ultimo_sobrenome = palavras[-1]
    primeiros_nomes = palavras[:-1]

    iniciais = []
    for nome in primeiros_nomes:
        if nome not in particulas:
            iniciais.append(f"{nome[0]}.")

    str_iniciais = " ".join(iniciais)

    if str_iniciais:
        return f"{ultimo_sobrenome}, {str_iniciais}"
    return ultimo_sobrenome


if __name__ == "__main__":
    nome_input = input("Digite o nome a ser formatado: ")
    resultado = formatar_nome(nome_input)
    print(resultado)
