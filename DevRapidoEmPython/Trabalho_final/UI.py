import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from database import Database
from regras import RegrasNegocio
from exp_csv import exportar_para_csv


class SupriDeskApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SupriDesk - Gestão de Solicitações Internas")
        self.root.geometry("920x560")
        self.root.minsize(850, 500)

        self.db = Database("solicitacoes.db")
        self.regras = RegrasNegocio(self.db)

        self._construir_interface()
        self.atualizar_tabela()

        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    def _construir_interface(self) -> None:
        # --- 1. Formulário de Cadastro ---
        frame_cadastro = ttk.LabelFrame(self.root, text="Nova Solicitação", padding=10)
        frame_cadastro.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(frame_cadastro, text="Setor:").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_setor = ttk.Entry(frame_cadastro, width=22)
        self.entry_setor.grid(row=0, column=1, padx=5)

        ttk.Label(frame_cadastro, text="Material:").grid(row=0, column=2, sticky="w", padx=5)
        self.entry_material = ttk.Entry(frame_cadastro, width=28)
        self.entry_material.grid(row=0, column=3, padx=5)

        ttk.Label(frame_cadastro, text="Quantidade:").grid(row=0, column=4, sticky="w", padx=5)
        self.entry_qtd = ttk.Entry(frame_cadastro, width=10)
        self.entry_qtd.grid(row=0, column=5, padx=5)

        ttk.Label(frame_cadastro, text="Prioridade:").grid(row=0, column=6, sticky="w", padx=5)
        self.combo_prioridade = ttk.Combobox(
            frame_cadastro,
            values=["Normal", "Alta"],
            state="readonly",
            width=10,
        )
        self.combo_prioridade.set("Normal")
        self.combo_prioridade.grid(row=0, column=7, padx=5)

        btn_cadastrar = ttk.Button(
            frame_cadastro,
            text="Cadastrar",
            command=self._acao_cadastrar,
        )
        btn_cadastrar.grid(row=0, column=8, padx=(10, 5))

        # --- 2. Barra de Pesquisa e Filtros ---
        frame_filtro = ttk.LabelFrame(self.root, text="Pesquisa e Filtros", padding=10)
        frame_filtro.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_filtro, text="Setor ou Material:").pack(side="left", padx=5)
        self.entry_busca = ttk.Entry(frame_filtro, width=30)
        self.entry_busca.pack(side="left", padx=5)

        ttk.Label(frame_filtro, text="Status:").pack(side="left", padx=(15, 5))
        self.combo_filtro_status = ttk.Combobox(
            frame_filtro,
            values=["Todos", "Pendente", "Em atendimento", "Atendida"],
            state="readonly",
            width=16,
        )
        self.combo_filtro_status.set("Todos")
        self.combo_filtro_status.pack(side="left", padx=5)

        ttk.Button(
            frame_filtro,
            text="Pesquisar",
            command=self.atualizar_tabela,
        ).pack(side="left", padx=(15, 5))

        ttk.Button(
            frame_filtro,
            text="Limpar Filtros",
            command=self._acao_limpar_filtros,
        ).pack(side="left", padx=5)

        # --- 3. Tabela (Treeview) ---
        frame_tabela = ttk.Frame(self.root, padding=(10, 5))
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("id", "setor", "material", "quantidade", "prioridade", "status", "data_hora")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

        cabecalhos = {
            "id": ("ID", 50),
            "setor": ("Setor", 130),
            "material": ("Material", 210),
            "quantidade": ("Qtd", 65),
            "prioridade": ("Prioridade", 90),
            "status": ("Status", 130),
            "data_hora": ("Data/Hora", 155),
        }

        for col, (texto, largura) in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            alinhamento = "center" if col in ("id", "quantidade", "prioridade", "status", "data_hora") else "w"
            self.tabela.column(col, width=largura, anchor=alinhamento)

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 4. Botões de Ação de Atendimento e Exportação ---
        frame_acoes = ttk.Frame(self.root, padding=10)
        frame_acoes.pack(fill="x")

        ttk.Button(
            frame_acoes,
            text="Iniciar Atendimento",
            command=self._acao_iniciar_atendimento,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            frame_acoes,
            text="Concluir Atendimento",
            command=self._acao_concluir_atendimento,
        ).pack(side="left", padx=8)

        ttk.Button(
            frame_acoes,
            text="Exportar CSV",
            command=self._acao_exportar_csv,
        ).pack(side="right")

    def _obter_id_selecionado(self) -> int | None:
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Seleção necessária", "Selecione uma solicitação na tabela.")
            return None
        valores = self.tabela.item(selecao[0], "values")
        return int(valores[0])

    def atualizar_tabela(self) -> None:
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        termo = self.entry_busca.get()
        status = self.combo_filtro_status.get()
        registros = self.regras.listar_pedidos(termo=termo, status=status)

        for linha in registros:
            self.tabela.insert("", "end", values=linha)

    def _acao_cadastrar(self) -> None:
        try:
            novo_id = self.regras.cadastrar_pedido(
                setor=self.entry_setor.get(),
                material=self.entry_material.get(),
                quantidade_texto=self.entry_qtd.get(),
                prioridade=self.combo_prioridade.get(),
            )
        except ValueError as erro:
            messagebox.showerror("Erro de Validação", str(erro))
            return

        self.entry_setor.delete(0, tk.END)
        self.entry_material.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.combo_prioridade.set("Normal")

        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", f"Solicitação #{novo_id} cadastrada com status 'Pendente'.")

    def _acao_iniciar_atendimento(self) -> None:
        pedido_id = self._obter_id_selecionado()
        if pedido_id is None:
            return

        try:
            self.regras.iniciar_atendimento(pedido_id)
        except ValueError as erro:
            messagebox.showerror("Operação Bloqueada", str(erro))
            return

        self.atualizar_tabela()

    def _acao_concluir_atendimento(self) -> None:
        pedido_id = self._obter_id_selecionado()
        if pedido_id is None:
            return

        try:
            self.regras.concluir_atendimento(pedido_id)
        except ValueError as erro:
            messagebox.showerror("Operação Bloqueada", str(erro))
            return

        self.atualizar_tabela()

    def _acao_limpar_filtros(self) -> None:
        self.entry_busca.delete(0, tk.END)
        self.combo_filtro_status.set("Todos")
        self.atualizar_tabela()

    def _acao_exportar_csv(self) -> None:
        termo = self.entry_busca.get()
        status = self.combo_filtro_status.get()
        registros = self.regras.listar_pedidos(termo=termo, status=status)

        if not registros:
            messagebox.showwarning("Exportação CSV", "Não há registros visíveis para exportar.")
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar histórico em CSV",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="historico_supridesk.csv",
        )
        if not caminho:
            return

        try:
            total = exportar_para_csv(caminho, registros)
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro ao Exportar", str(erro))
            return

        messagebox.showinfo("Exportação Concluída", f"{total} registro(s) exportado(s) com sucesso.")

    def _ao_fechar(self) -> None:
        self.db.fechar()
        self.root.destroy()


if __name__ == "__main__":
    janela = tk.Tk()
    app = SupriDeskApp(janela)
    janela.mainloop()
