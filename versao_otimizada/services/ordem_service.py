from math import isfinite

from algoritmos.ordenacao import (
    ordenar_por_prioridade,
    ordenar_por_valor,
    ordenar_por_chegada
)

from models.ordem_servico import OrdemServico
from dados.ordens import ordens
from estruturas.fila_prioridade import FilaPrioridade

fila_ordens = FilaPrioridade()

#cadastro e ordem de serviço
def cadastrar_ordem():
    print("\n--- CADASTRO DE ORDEM DE SERVIÇO ---")

    codigo = int(input("Código da OS: "))

    if ordens.buscar(codigo) is not None:
        print("Já existe uma ordem com esse código.")
        return

    cliente = input("Nome do cliente: ")
    veiculo = input("Veículo: ")
    problema = input("Problema apresentado: ")

    prioridade = int(input("Prioridade (1 a 5): "))

    if prioridade < 1 or prioridade > 5:
        print("Prioridade inválida.")
        return

    nova_ordem = OrdemServico(
        codigo,
        cliente,
        veiculo,
        problema,
        prioridade
    )

    ordens.inserir(codigo, nova_ordem)
    fila_ordens.inserir(nova_ordem)

    print("Ordem de serviço cadastrada com sucesso!")

#listamento de todas as ordens
def listar_ordens():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    print("\n--- ORDENS DE SERVIÇO ---")

    #mesma ordem de cadastro da versão base
    for ordem in ordenar_por_chegada(ordens.em_ordem()):
        print("\n-------------------------")
        print("Código:", ordem.codigo)
        print("Cliente:", ordem.cliente)
        print("Veículo:", ordem.veiculo)
        print("Problema:", ordem.problema)
        print("Prioridade:", ordem.prioridade)
        print("Status:", ordem.status)
        print(f"Valor: R$ {ordem.valor_total:.2f}")

#consultar uma OS (ordem de serviço)
def consultar_ordem():
    try:
    codigo = int(input("Código da OS: "))

except ValueError:
    print("Digite um código numérico válido.")
    return

    ordem = ordens.buscar(codigo)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    print("\n--- ORDEM ENCONTRADA ---")
    print("Código:", ordem.codigo)
    print("Cliente:", ordem.cliente)
    print("Veículo:", ordem.veiculo)
    print("Problema:", ordem.problema)
    print("Prioridade:", ordem.prioridade)
    print("Status:", ordem.status)
    print(f"Valor: R$ {ordem.valor_total:.2f}")

def alterar_status():
    try:
        codigo = int(input("Código da OS: "))
    except ValueError:
        print("Código inválido.")
        return

    ordem = ordens.buscar(codigo)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    print("\nStatus atual:", ordem.status)

    print("1 - Aguardando")
    print("2 - Em manutenção")
    print("3 - Concluída")

    opcao = input("Novo status: ").strip()

    if opcao == "1":
        novo_status = "Aguardando"

    elif opcao == "2":
        novo_status = "Em manutenção"

    elif opcao == "3":
        novo_status = "Concluída"

    else:
        print("Opção inválida.")
        return

    ordem.alterar_status(novo_status)

    # Sincronização com o heap
    if novo_status == "Aguardando":

        if ordem.pos_fila == -1:
            fila_ordens.inserir(ordem)

    else:
        fila_ordens.remover(ordem)

    print("Status alterado com sucesso!")
def alterar_prioridade():
    codigo = int(input("Código da OS: "))

    ordem = ordens.buscar(codigo)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    print("Prioridade atual:", ordem.prioridade)

    nova_prioridade = int(input("Nova prioridade (1 a 5): "))

    if nova_prioridade < 1 or nova_prioridade > 5:
        print("Prioridade inválida.")
        return

    ordem.alterar_prioridade(nova_prioridade)
    fila_ordens.atualizar_prioridade(ordem)

    print("Prioridade alterada com sucesso!")

#registrar serviço
def registrar_servico():
    try:
        codigo = int(input("Código da OS: "))
    except ValueError:
        print("Código inválido.")
        return

    ordem = ordens.buscar(codigo)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    descricao = input("Descrição do serviço: ").strip()

    if not descricao:
        print("A descrição é obrigatória.")
        return

    try:
        valor_texto = input("Valor do serviço: R$ ")
        valor = float(valor_texto.replace(",", "."))

    except ValueError:
        print("Valor inválido.")
        return

    if valor < 0 or not isfinite(valor):
        print("Valor inválido.")
        return

    ordem.adicionar_servico(descricao, valor)

    print("Serviço registrado com sucesso!")
    print(f"Valor atual da OS: R$ {ordem.valor_total:.2f}")
def remover_ordem():
    codigo = int(input("Código da OS que deseja remover: "))

    ordem = ordens.buscar(codigo)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    ordens.remover(codigo)

    fila_ordens.remover(ordem)

    print("Ordem removida com sucesso!")

#processamento da próxima ordem
def processar_proxima_ordem():
    ordem = fila_ordens.remover_maior_prioridade()

    if ordem is None:
        print("Não existem ordens aguardando atendimento.")
        return

    ordem.alterar_status("Em manutenção")

    print("\n--- PRÓXIMA ORDEM ---")
    print("Código:", ordem.codigo)
    print("Cliente:", ordem.cliente)
    print("Veículo:", ordem.veiculo)
    print("Problema:", ordem.problema)
    print("Prioridade:", ordem.prioridade)
    print("Status:", ordem.status)

#relatório por prioridade
def relatorio_por_prioridade():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    ordenadas = ordenar_por_prioridade(ordens.em_ordem())

    print("\n--- RELATÓRIO POR PRIORIDADE ---")

    for ordem in ordenadas:
        print(
            "OS",
            ordem.codigo,
            "| Prioridade:",
            ordem.prioridade,
            "| Cliente:",
            ordem.cliente
        )

#relatório por valor
def relatorio_por_valor():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    ordenadas = ordenar_por_valor(ordens.em_ordem())

    print("\n--- RELATÓRIO POR VALOR ---")

    for ordem in ordenadas:
        print(
            "OS",
            ordem.codigo,
            "| Cliente:",
            ordem.cliente,
            f"| Valor: R$ {ordem.valor_total:.2f}"
        )

#travessias da árvore AVL (nível 0 = raiz)
def mostrar_travessia(titulo, itens, identar):
    print(f"\n--- {titulo} ---")

    for nivel, ordem in itens:
        recuo = "    " * nivel if identar else ""

        print(
            recuo + "OS",
            ordem.codigo,
            "| Cliente:",
            ordem.cliente,
            "| Prioridade:",
            ordem.prioridade,
            "| Nível:",
            nivel
        )

#em ordem: esquerda, raiz, direita (códigos crescentes)
def exibir_em_ordem():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    mostrar_travessia(
        "TRAVESSIA EM ORDEM (CÓDIGOS CRESCENTES)",
        ordens.em_ordem(com_nivel=True),
        False
    )

#pré-ordem: raiz, esquerda, direita (hierarquia a partir da raiz)
def exibir_pre_ordem():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    mostrar_travessia(
        "TRAVESSIA PRÉ-ORDEM (HIERARQUIA A PARTIR DA RAIZ)",
        ordens.pre_ordem(com_nivel=True),
        True
    )

#pós-ordem: esquerda, direita, raiz (filhos antes do pai)
def exibir_pos_ordem():
    if len(ordens) == 0:
        print("Nenhuma ordem cadastrada.")
        return

    mostrar_travessia(
        "TRAVESSIA PÓS-ORDEM (FILHOS ANTES DO PAI)",
        ordens.pos_ordem(com_nivel=True),
        False
    )
