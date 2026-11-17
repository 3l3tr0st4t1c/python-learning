import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_name: str = "solicitacoes.db") -> None:
        base_dir = Path(__file__).resolve().parent
        self.db_path = base_dir / db_name
        self.conn = sqlite3.connect(self.db_path)
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setor TEXT NOT NULL,
                    material TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    prioridade TEXT NOT NULL,
                    status TEXT NOT NULL,
                    data_hora TEXT NOT NULL
                )
                """
            )

    def inserir(self, setor: str, material: str, quantidade: int, prioridade: str, status: str, data_hora: str,) -> int:
        with self.conn:
            cursor = self.conn.execute(
                """
                INSERT INTO pedidos (setor, material, quantidade, prioridade, status, data_hora)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (setor, material, quantidade, prioridade, status, data_hora),
            )
            return cursor.lastrowid

    def listar(self, termo: str = "", status: str = "") -> list[tuple]:
        query = """
            SELECT id, setor, material, quantidade, prioridade, status, data_hora
            FROM pedidos
            WHERE 1=1
        """
        params: list[str] = []

        if termo.strip():
            query += " AND (setor LIKE ? OR material LIKE ?)"
            like_termo = f"%{termo.strip()}%"
            params.extend([like_termo, like_termo])

        if status.strip() and status != "Todos":
            query += " AND status = ?"
            params.append(status.strip())

        query += " ORDER BY id DESC"
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def buscar_por_id(self, pedido_id: int) -> tuple | None:
        cursor = self.conn.execute(
            """
            SELECT id, setor, material, quantidade, prioridade, status, data_hora
            FROM pedidos
            WHERE id = ?
            """,
            (pedido_id,),
        )
        return cursor.fetchone()

    def atualizar_status(self, pedido_id: int, novo_status: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE pedidos SET status = ? WHERE id = ?",
                (novo_status, pedido_id),
            )

    def fechar(self) -> None:
        self.conn.close() 
