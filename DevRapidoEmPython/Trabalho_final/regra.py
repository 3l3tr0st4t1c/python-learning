from datetime import datetime
from database import Database


class RegrasNegocio:
    PRIORIDADES_VALIDAS = ("Normal", "Alta")
    STATUS_INICIAL = "Pendente"

    TRANSICOES_PERMITIDAS = {
        "Pendente": "Em atendimento",
        "Em atendimento": "Atendida",
    }

    def __init__(self, db: Database) -> None:
        self.db = db

    def cadastrar_pedido(self, setor: str, material: str, quantidade_texto: str, prioridade: str,) -> int:
        setor_limpo = setor.strip()
        material_limpo = material.strip()
        qtd_limpa = quantidade_texto.strip()
        prioridade_limpa = prioridade.strip()

        if not setor_limpo:
            raise ValueError("O campo 'Setor' não pode ficar vazio.")

        if not material_limpo:
            raise ValueError("O campo 'Material' não pode ficar vazio.")

        if not qtd_limpa:
            raise ValueError("O campo 'Quantidade' não pode ficar vazio.")

        try:
            quantidade = int(qtd_limpa)
        except ValueError:
            raise ValueError("A quantidade deve ser um número inteiro válido.")

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser um inteiro maior que zero.")

        if prioridade_limpa not in self.PRIORIDADES_VALIDAS:
            raise ValueError("Prioridade inválida. Selecione 'Normal' ou 'Alta'.")

        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self.db.inserir(
            setor=setor_limpo,
            material=material_limpo,
            quantidade=quantidade,
            prioridade=prioridade_limpa,
            status=self.STATUS_INICIAL,
            data_hora=data_hora,
        )

    def listar_pedidos(self, termo: str = "", status: str = "") -> list[tuple]:
        return self.db.listar(termo=termo, status=status)

    def iniciar_atendimento(self, pedido_id: int) -> None:
        self._alterar_status(pedido_id, status_destino="Em atendimento")

    def concluir_atendimento(self, pedido_id: int) -> None:
        self._alterar_status(pedido_id, status_destino="Atendida")

    def _alterar_status(self, pedido_id: int, status_destino: str) -> None:
        registro = self.db.buscar_por_id(pedido_id)
        if registro is None:
            raise ValueError(f"Pedido #{pedido_id} não encontrado no banco.")

        status_atual = registro[5]

        if status_atual == status_destino:
            raise ValueError(
                f"Operação bloqueada: o pedido #{pedido_id} já está '{status_atual}'."
            )

        proximo_valido = self.TRANSICOES_PERMITIDAS.get(status_atual)
        if proximo_valido != status_destino:
            raise ValueError(
                f"Transição inválida: não é permitido mudar de '{status_atual}' para '{status_destino}'."
            )

        self.db.atualizar_status(pedido_id, status_destino)
