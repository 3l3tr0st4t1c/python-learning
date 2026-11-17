import os
from database import Database
from regras import RegrasNegocio

# Usa um banco temporário só para não sujar o oficial
ARQUIVO_TESTE = "teste_temp.db"
if os.path.exists(ARQUIVO_TESTE):
    os.remove(ARQUIVO_TESTE)

db = Database(ARQUIVO_TESTE)
regras = RegrasNegocio(db)

# Teste 1: Cadastro válido inicia como Pendente
id_pedido = regras.cadastrar_pedido("TI", "Mouse USB", "5", "Alta")
registro = db.buscar_por_id(id_pedido)
assert registro[5] == "Pendente", "Deveria iniciar como Pendente"

# Teste 2: Quantidade 0 deve ser recusada
try:
    regras.cadastrar_pedido("Administrativo", "Papel A4", "0", "Normal")
    assert False, "Deveria ter bloqueado quantidade 0"
except ValueError:
    pass  # Bloqueou corretamente

# Teste 3: Fluxo Pendente -> Em atendimento -> Atendida e bloqueio de repetição
regras.iniciar_atendimento(id_pedido)
regras.concluir_atendimento(id_pedido)
try:
    regras.concluir_atendimento(id_pedido)
    assert False, "Deveria ter bloqueado conclusão repetida"
except ValueError:
    pass  # Bloqueou corretamente

db.fechar()
os.remove(ARQUIVO_TESTE)
print("Todos os testes passaram!")
