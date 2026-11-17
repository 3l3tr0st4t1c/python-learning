import csv


CABECALHO_CSV = [
    "ID",
    "Setor",
    "Material",
    "Quantidade",
    "Prioridade",
    "Status",
    "Data/Hora",
]


def exportar_para_csv(caminho_arquivo: str, registros: list[tuple]) -> int:
    if not registros:
        raise ValueError("Não há solicitações na tabela para exportar.")

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(CABECALHO_CSV)
        writer.writerows(registros)

    return len(registros)
