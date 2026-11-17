import sqlite3
from pathlib import Path


class Database:



    def __init__(self, caminho: str | Path = "usuarios.db") -> None:
        self.conn = sqlite3.connect(caminho)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        self.conn.commit()

    def listar(self) -> list[tuple[int, str, str]]:
        cursor = self.conn.execute(
            "SELECT id, nome, email FROM usuarios ORDER BY nome"
        )
        return cursor.fetchall()

    def inserir(self, nome: str, email: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
                (nome, email),
            )

    def atualizar(self, usuario_id: int, nome: str, email: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
                (nome, email, usuario_id),
            )

    def excluir(self, usuario_id: int) -> None:
        with self.conn:
            self.conn.execute(
                "DELETE FROM usuarios WHERE id = ?", (usuario_id,)
            )
        
    def pesquisar_termo(self,nome:str):
        with self.conn:
           cursor=self.conn.execute(
                "SELECT id, nome,email WHERE nome LIKE ?",(f"%{nome}%",)
            )
        return cursor.fetchall()

    def fechar(self) -> None:
        self.conn.close()


bancodir=Path(__file__).resolve().parent/"DB"
bancodir.mkdir(exist_ok=True)

class Banco:
    

    def __init__(self):
        
        self.conexao=sqlite3.connect(bancodir/"solicitacoes.db")
        self.cursor = self.conexao.cursor()
        try:
                self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS pedidos (
                    id PRIMARY KEY,
                    setor TEXT NOT NULL,
                    material TEXT NOT NULL,
                    qtd INTEGER NOT NULL,
                    prio BOOLEAN NOT NULL
                )
            """
            )
                self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro no banco de dados ao criar, {e}!")




    def update(self):
        self.cursor.execute (
            with
        )
