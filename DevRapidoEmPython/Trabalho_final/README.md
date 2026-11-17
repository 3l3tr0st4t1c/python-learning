# SupriDesk — Gestão de Solicitações Internas

Sistema desktop desenvolvido em Python para organizar pedidos internos de materiais (cabos, periféricos, papel e itens de escritório), controlar o fluxo de atendimento e manter um histórico persistente com exportação para CSV.

Projeto desenvolvido para a disciplina **Desenvolvimento Rápido de Aplicações em Python (2026.2)**.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3 (testado em Python 3.10+)
* **Interface Gráfica:** `tkinter` e `tkinter.ttk` (biblioteca padrão)
* **Banco de Dados:** `sqlite3` (biblioteca padrão, com consultas parametrizadas)
* **Exportação de Dados:** `csv` (biblioteca padrão)

> **Nota:** O projeto utiliza apenas módulos nativos da biblioteca padrão do Python, não sendo necessária a instalação de pacotes externos via `pip`.

---

## Estrutura do Projeto

``` text
SupriDesk/
├── main.py          # Ponto de entrada (python3 main.py)
├── UI.py            # Interface gráfica Tkinter/ttk
├── regras.py        # Validações e máquina de estados do atendimento
├── database.py      # Persistência SQLite com consultas parametrizadas
├── exp_csv.py       # Exportação do histórico para CSV
 README.md        # Documentação, testes e declaração de autoria

```


*(O arquivo `solicitacoes.db` é criado automaticamente na raiz do projeto na primeira execução do sistema.)*

---

## Como Executar

1. Clone este repositório ou baixe os arquivos para uma pasta local:
   ```bash
   git clone https://github.com/3l3tr0st4t1c/python-learning/edit/main/DevRapidoEmPython/Trabalho_final/
   cd Trabalho_final
   ```

2. Execute a aplicação principal:
   ```bash
   python main.py
   ```
   *(Em ambientes Linux/macOS, utilize `python3 main.py` caso necessário.)*

3. Para rodar a verificação rápida das regras de negócio no terminal:
   ```bash
   python teste_rapido.py
   ```

---

## Funcionalidades

* **Cadastro com Validação:** Registro de *Setor*, *Material*, *Quantidade* (inteiro positivo) e *Prioridade* (`Normal` ou `Alta`), gerando `ID`, `Data/Hora` e status inicial `Pendente` automaticamente.
* **Persistência em SQLite:** Criação automática do banco `solicitacoes.db` e operações realizadas exclusivamente com SQL parametrizado (`?`).
* **Fluxo de Atendimento Controlado:** Máquina de estados que permite apenas a sequência `Pendente` $\rightarrow$ `Em atendimento` $\rightarrow$ `Atendida`, bloqueando saltos de etapa ou ações repetidas.
* **Pesquisa e Filtros:** Busca textual por *Setor* ou *Material*, combinada com filtro por *Status* e botão para limpar os filtros.
* **Exportação CSV:** Geração de arquivo `.csv` com cabeçalho (`ID`, `Setor`, `Material`, `Quantidade`, `Prioridade`, `Status`, `Data/Hora`) contendo os registros exibidos na tabela.

---

## Testes Documentados

Os cenários abaixo foram executados para validar o funcionamento do sistema conforme os requisitos da atividade:

| # | Cenário de Teste | Entrada / Ação | Resultado Esperado | Status |
|---|---|---|---|---|
| **1** | **Cadastro válido** | Cadastrar `TI` / `Mouse USB` / `5` / `Alta` | Solicitação registrada na tabela com `ID` automático, data/hora atual e status `Pendente`. | Aprovado |
| **2** | **Validação de quantidade** | Tentar cadastrar `Administrativo` / `Papel A4` / `0` / `Normal` | Operação recusada com mensagem de erro informando que a quantidade deve ser um inteiro maior que zero. | Aprovado |
| **3** | **Fluxo e bloqueio de repetição** | Selecionar o pedido: `Pendente` $\rightarrow$ *Iniciar Atendimento* (`Em atendimento`) $\rightarrow$ *Concluir Atendimento* (`Atendida`) $\rightarrow$ tentar *Concluir Atendimento* novamente | O status avança corretamente até `Atendida`, e a segunda tentativa de conclusão é bloqueada com alerta. | Aprovado |
| **4** | **Persistência após reinício** | Fechar a janela do SupriDesk e executar `python main.py` novamente | Os registros cadastrados e seus respectivos status permanecem salvos no banco `solicitacoes.db`. | Aprovado |
| **5** | **Pesquisa, filtro e CSV** | Pesquisar por `Mouse` ou `TI`, selecionar filtro de status `Atendida` e clicar em *Exportar CSV* | A tabela exibe apenas os registros filtrados e gera um arquivo `.csv` válido com cabeçalho e dados correspondentes. | Aprovado |

---

## Autoria e Uso de Ferramentas de IA

Trabalho desenvolvido individualmente para avaliação da disciplina. Em conformidade com as diretrizes de transparência do trabalho, registra-se que a ferramenta de IA generativa **Gemini** foi utilizada como apoio técnico durante o desenvolvimento nas seguintes frentes:

* **Alinhamento aos requisitos e revisão do banco de dados:** Apoio na correção da estrutura inicial da camada SQLite e adequação das colunas e regras aos requisitos especificados no enunciado.
* **Construção da interface gráfica (`main.py`):** Geração e organização dos componentes visuais em `Tkinter`/`ttk.Treeview` e integração com os eventos da camada de regras.
* **Testes e documentação:** Estruturação do script de validação (`teste_rapido.py`) e organização deste `README.md`.
