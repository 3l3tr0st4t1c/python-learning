import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from database import Database
from regras import RegrasNegocio
from exp_csv import exportar_para_csv


class SupriDeskApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SupriDesk | Gestão de Suprimentos")
        self.root.geometry("1100x700")
        self.root.minsize(900, 580)
        self.root.configure(bg="#F1F5F9")

        self.db = Database("solicitacoes.db")
        self.regras = RegrasNegocio(self.db)

        self._configurar_estilo()
        self._construir_interface()
        self.atualizar_tabela()

        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    def _configurar_estilo(self) -> None:
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#334155",
            rowheight=36,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10),
            borderwidth=0
        )

        estilo.configure(
            "Treeview.Heading",
            background="#1E293B",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=11,
            relief="flat"
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", "#1E293B")]
        )

        estilo.configure(
            "TEntry",
            padding=9,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "TCombobox",
            padding=9,
            font=("Segoe UI", 10)
        )

    def _construir_interface(self) -> None:
        cabecalho = tk.Frame(self.root, bg="#0F172A", height=105)
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        tk.Label(
            cabecalho,
            text="SupriDesk",
            font=("Segoe UI", 26, "bold"),
            bg="#0F172A",
            fg="#FFFFFF"
        ).pack(anchor="w", padx=28, pady=(15, 0))

        tk.Label(
            cabecalho,
            text="Sistema de gerenciamento de solicitações internas",
            font=("Segoe UI", 10),
            bg="#0F172A",
            fg="#94A3B8"
        ).pack(anchor="w", padx=31)

        conteudo = tk.Frame(self.root, bg="#F1F5F9")
        conteudo.pack(fill="both", expand=True, padx=20, pady=15)

        self._criar_cadastro(conteudo)
        self._criar_filtros(conteudo)
        self._criar_tabela(conteudo)
        self._criar_acoes(conteudo)

    def _criar_cadastro(self, pai) -> None:
        frame = tk.Frame(
            pai,
            bg="#FFFFFF",
            padx=20,
            pady=16
        )
        frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            frame,
            text="Nova solicitação",
            font=("Segoe UI", 15, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        ).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 15))

        campos = [
            ("Setor", 0),
            ("Material", 1),
            ("Quantidade", 2),
            ("Prioridade", 3)
        ]

        for texto, coluna in campos:
            tk.Label(
                frame,
                text=texto,
                font=("Segoe UI", 9, "bold"),
                bg="#FFFFFF",
                fg="#475569"
            ).grid(row=1, column=coluna, sticky="w", padx=(0, 10))

        self.entry_setor = ttk.Entry(frame)
        self.entry_setor.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=5)

        self.entry_material = ttk.Entry(frame)
        self.entry_material.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=5)

        self.entry_qtd = ttk.Entry(frame)
        self.entry_qtd.grid(row=2, column=2, sticky="ew", padx=(0, 10), pady=5)

        self.combo_prioridade = ttk.Combobox(
            frame,
            values=["Normal", "Alta"],
            state="readonly"
        )
        self.combo_prioridade.set("Normal")
        self.combo_prioridade.grid(row=2, column=3, sticky="ew", padx=(0, 10), pady=5)

        self._criar_botao(
            frame,
            "＋ Cadastrar pedido",
            self._acao_cadastrar,
            "#2563EB"
        ).grid(row=2, column=4, sticky="ew", pady=5)

        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)

    def _criar_filtros(self, pai) -> None:
        frame = tk.Frame(
            pai,
            bg="#FFFFFF",
            padx=20,
            pady=15
        )
        frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            frame,
            text="Pesquisa e filtros",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        tk.Label(
            frame,
            text="Setor ou material",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        ).grid(row=1, column=0, sticky="w")

        tk.Label(
            frame,
            text="Status",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        ).grid(row=1, column=1, sticky="w")

        self.entry_busca = ttk.Entry(frame)
        self.entry_busca.grid(row=2, column=0, sticky="ew", padx=(0, 12), pady=5)

        self.combo_filtro_status = ttk.Combobox(
            frame,
            values=["Todos", "Pendente", "Em atendimento", "Atendida"],
            state="readonly"
        )
        self.combo_filtro_status.set("Todos")
        self.combo_filtro_status.grid(row=2, column=1, sticky="ew", padx=(0, 12), pady=5)

        self._criar_botao(
            frame,
            "Pesquisar",
            self.atualizar_tabela,
            "#2563EB"
        ).grid(row=2, column=2, padx=5)

        self._criar_botao(
            frame,
            "Limpar filtros",
            self._acao_limpar_filtros,
            "#E2E8F0",
            "#334155"
        ).grid(row=2, column=3, padx=5)

        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=1)

    def _criar_tabela(self, pai) -> None:
        frame = tk.Frame(
            pai,
            bg="#FFFFFF",
            padx=15,
            pady=15
        )
        frame.pack(fill="both", expand=True, pady=(0, 12))

        tk.Label(
            frame,
            text="Histórico de solicitações",
            font=("Segoe UI", 15, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        ).pack(anchor="w", pady=(0, 12))

        area = tk.Frame(frame, bg="#FFFFFF")
        area.pack(fill="both", expand=True)

        colunas = (
            "id",
            "setor",
            "material",
            "quantidade",
            "prioridade",
            "status",
            "data_hora"
        )

        self.tabela = ttk.Treeview(
            area,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        cabecalhos = {
            "id": ("ID", 50),
            "setor": ("Setor", 130),
            "material": ("Material", 210),
            "quantidade": ("Quantidade", 90),
            "prioridade": ("Prioridade", 100),
            "status": ("Status", 140),
            "data_hora": ("Data/Hora", 160)
        }

        for coluna, (titulo, largura) in cabecalhos.items():
            alinhamento = "center" if coluna in (
                "id",
                "quantidade",
                "prioridade",
                "status",
                "data_hora"
            ) else "w"

            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(
                coluna,
                width=largura,
                minwidth=45,
                anchor=alinhamento
            )

        scrollbar = ttk.Scrollbar(
            area,
            orient="vertical",
            command=self.tabela.yview
        )

        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabela.tag_configure("par", background="#F8FAFC")
        self.tabela.tag_configure("impar", background="#FFFFFF")

    def _criar_acoes(self, pai) -> None:
        frame = tk.Frame(pai, bg="#F1F5F9")
        frame.pack(fill="x", pady=(0, 5))

        self._criar_botao(
            frame,
            "▶ Iniciar atendimento",
            self._acao_iniciar_atendimento,
            "#D97706"
        ).pack(side="left", padx=(0, 8))

        self._criar_botao(
            frame,
            "✓ Concluir atendimento",
            self._acao_concluir_atendimento,
            "#16A34A"
        ).pack(side="left", padx=8)

        self._criar_botao(
            frame,
            "↓ Exportar CSV",
            self._acao_exportar_csv,
            "#475569"
        ).pack(side="right")

    def _criar_botao(
        self,
        pai,
        texto,
        comando,
        cor,
        cor_texto="#FFFFFF"
    ):
        return tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=cor,
            fg=cor_texto,
            activebackground=cor,
            activeforeground=cor_texto,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9,
            bd=0
        )

    def _obter_id_selecionado(self) -> int | None:
        selecao = self.tabela.selection()

        if not selecao:
            messagebox.showwarning(
                "Seleção necessária",
                "Selecione uma solicitação na tabela."
            )
            return None

        valores = self.tabela.item(selecao[0], "values")
        return int(valores[0])

    def atualizar_tabela(self) -> None:
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        termo = self.entry_busca.get()
        status = self.combo_filtro_status.get()

        registros = self.regras.listar_pedidos(
            termo=termo,
            status=status
        )

        for indice, linha in enumerate(registros):
            tag = "par" if indice % 2 == 0 else "impar"

            self.tabela.insert(
                "",
                "end",
                values=linha,
                tags=(tag,)
            )

    def _acao_cadastrar(self) -> None:
        try:
            novo_id = self.regras.cadastrar_pedido(
                setor=self.entry_setor.get(),
                material=self.entry_material.get(),
                quantidade_texto=self.entry_qtd.get(),
                prioridade=self.combo_prioridade.get()
            )

        except ValueError as erro:
            messagebox.showerror("Erro de Validação", str(erro))
            return

        self.entry_setor.delete(0, tk.END)
        self.entry_material.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.combo_prioridade.set("Normal")

        self.atualizar_tabela()

        messagebox.showinfo(
            "Sucesso",
            f"Solicitação #{novo_id} cadastrada com status 'Pendente'."
        )

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

        registros = self.regras.listar_pedidos(
            termo=termo,
            status=status
        )

        if not registros:
            messagebox.showwarning(
                "Exportação CSV",
                "Não há registros visíveis para exportar."
            )
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar histórico em CSV",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="historico_supridesk.csv"
        )

        if not caminho:
            return

        try:
            total = exportar_para_csv(caminho, registros)

        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro ao Exportar", str(erro))
            return

        messagebox.showinfo(
            "Exportação Concluída",
            f"{total} registro(s) exportado(s) com sucesso."
        )

    def _ao_fechar(self) -> None:
        self.db.fechar()
        self.root.destroy()
