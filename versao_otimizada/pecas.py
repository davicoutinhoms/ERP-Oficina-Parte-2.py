pecas = []
historico_movimentacoes = []
from math import isfinite

def menu():
    while True:
        print("\n===== SISTEMA DE CADASTRO DE PEÇAS VEICULARES =====")
        print("1 - Cadastrar peça")
        print("2 - Buscar peça")
        print("3 - Alterar peça")
        print("4 - Remover peça")
        print("5 - Entrada de estoque")
        print("6 - Saída de estoque")
        print("7 - Exibir histórico de movimentações")
        print("8 - Desfazer última movimentação")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastro_pecas()
        elif opcao == '2':
            busca_pecas()
        elif opcao == '3':
            alteracao_pecas()
        elif opcao == '4':
            remocao_pecas()
        elif opcao == '5':
            entrada_estoque()
        elif opcao == '6':
            saida_estoque()
        elif opcao == '7':
            exibir_historico()
        elif opcao == '8':
            desfazer_ultima_movimentacao()
        elif opcao == '0':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")


def cadastro_pecas():
    print('CADASTRO DE PEÇAS')

    peca = input('Peça veicular: ').strip()

    if not peca:
        print('O cadastro é obrigatório!')
        return

    if buscar_peca(peca) is not None:
        print('Essa peça já está cadastrada!')
        return

    try:
        quantidade = int(input('Quantidade em estoque: '))
        valor = float(input('Valor da peça: R$ ').replace(',', '.'))
    except ValueError:
        print('Quantidade ou valor inválido!')
        return

    if quantidade < 0 or valor < 0 or not isfinite(valor):
        print('Quantidade ou valor inválido!')
        return

    peca_new = {
        'Peça: ': peca,
        'Quantidade: ': quantidade,
        'Preço: R$': valor,
    }

    esquerda = 0
    direita = len(pecas)

    while esquerda < direita:
        meio = (esquerda + direita) // 2

        if pecas[meio]['Peça: '].casefold() < peca.casefold():
            esquerda = meio + 1
        else:
            direita = meio

    pecas.insert(esquerda, peca_new)

    print('Peça cadastrada!')


def ordenar_pecas():
    n = len(pecas)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if pecas[j]['Peça: '] > pecas[j + 1]['Peça: ']:
                pecas[j], pecas[j + 1] = pecas[j + 1], pecas[j]
    return pecas


def busca_binaria(nome_procurado):
    nome_procurado = nome_procurado.strip().casefold()

    esquerda = 0
    direita = len(pecas) - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome_meio = pecas[meio]['Peça: '].casefold()

        if nome_meio == nome_procurado:
            return meio

        elif nome_meio < nome_procurado:
            esquerda = meio + 1

        else:
            direita = meio - 1

    return -1


def buscar_peca(nome_procurado):
    indice = busca_binaria(nome_procurado)

    if indice == -1:
        return None

    return pecas[indice]


def busca_pecas():
    print("BUSCA DE PEÇA")

    if len(pecas) == 0:
        print("Nenhuma peça cadastrada!")
        return

    nome_pecas = input("Qual o nome da peça: ")
    peca_encontrada = buscar_peca(nome_pecas)

    if peca_encontrada is None:
        print("Peça não encontrada!")
        return

    print(f"Peça: {peca_encontrada['Peça: ']}")
    print(f"Quantidade: {peca_encontrada['Quantidade: ']}")
    print(f"Preço: R$ {peca_encontrada['Preço: R$']}")


def alteracao_pecas():
    print('ALTERAÇÃO DE PEÇA')

    nome_procurado = input('Qual peça você quer alterar: ')
    peca_encontrada = buscar_peca(nome_procurado)

    if peca_encontrada is None:
        print('Peça não encontrada!')
        return

    nova_quantidade = input('Nova quantidade: ').strip()
    novo_valor = input('Novo valor: ').strip()

    try:
        quantidade = (
            int(nova_quantidade)
            if nova_quantidade
            else peca_encontrada['Quantidade: ']
        )

        valor = (
            float(novo_valor.replace(',', '.'))
            if novo_valor
            else peca_encontrada['Preço: R$']
        )

    except ValueError:
        print('Valor ou quantidade inválida!')
        return

    if quantidade < 0 or valor < 0 or not isfinite(valor):
        print('Quantidade ou valor inválido!')
        return

    peca_encontrada['Quantidade: '] = quantidade
    peca_encontrada['Preço: R$'] = valor

    print('Peça alterada com sucesso!')


def remocao_pecas():
    print('REMOÇÃO DE PEÇA')

    nome_procurado = input('Qual peça você quer remover: ')
    ordenar_pecas()
    indice_encontrado = busca_binaria(nome_procurado)

    if indice_encontrado == -1:
        print('Peça não encontrada!')
    else:
        confirmacao = input(f"Tem certeza que deseja remover '{nome_procurado}'? (s/n): ")
        if confirmacao.lower() == 's':
            pecas.pop(indice_encontrado)
            print('Peça removida com sucesso!')
        else:
            print('Remoção cancelada.')


def entrada_estoque():
    print('ENTRADA DE PEÇAS NO ESTOQUE')

    nome_procurado = input('Qual peça está entrando: ')
    peca_encontrada = buscar_peca(nome_procurado)

    if peca_encontrada is None:
        print('Peça não encontrada!')
        return

    quantidade_entrada = int(input('Quantidade que está entrando: '))

    if quantidade_entrada <= 0:
        print('A quantidade precisa ser maior que zero!')
        return

    peca_encontrada['Quantidade: '] += quantidade_entrada

    historico_movimentacoes.append({
        'tipo': 'entrada',
        'peca': nome_procurado,
        'quantidade': quantidade_entrada,
    })

    print(f'Entrada registrada! Novo estoque de {nome_procurado}: {peca_encontrada["Quantidade: "]}')


def saida_estoque():
    print('SAÍDA DE PEÇAS DO ESTOQUE')

    nome_procurado = input('Qual peça está saindo: ')
    peca_encontrada = buscar_peca(nome_procurado)

    if peca_encontrada is None:
        print('Peça não encontrada!')
        return

    quantidade_saida = int(input('Quantidade que está saindo: '))

    if quantidade_saida <= 0:
        print('A quantidade precisa ser maior que zero!')
        return

    if quantidade_saida > peca_encontrada['Quantidade: ']:
        print(f'Estoque insuficiente! Só existem {peca_encontrada["Quantidade: "]} unidade(s).')
        return

    peca_encontrada['Quantidade: '] -= quantidade_saida

    historico_movimentacoes.append({
        'tipo': 'saida',
        'peca': nome_procurado,
        'quantidade': quantidade_saida,
    })

    print(f'Saída registrada! Novo estoque de {nome_procurado}: {peca_encontrada["Quantidade: "]}')


def exibir_historico():
    print('HISTÓRICO DE MOVIMENTAÇÕES')

    if len(historico_movimentacoes) == 0:
        print('Nenhuma movimentação registrada ainda.')
        return

    for movimento in reversed(historico_movimentacoes):
        print(f"{movimento['tipo'].upper()} - {movimento['peca']} - {movimento['quantidade']} unidade(s)")


def desfazer_ultima_movimentacao():
    print('DESFAZER ÚLTIMA MOVIMENTAÇÃO')

    if not historico_movimentacoes:
        print('Não há movimentações para desfazer.')
        return

    # Consulta o topo da pilha sem remover
    ultimo_movimento = historico_movimentacoes[-1]

    peca_encontrada = buscar_peca(
        ultimo_movimento['peca']
    )

    if peca_encontrada is None:
        print('A peça não existe mais no cadastro.')
        return

    quantidade = ultimo_movimento['quantidade']

    if ultimo_movimento['tipo'] == 'entrada':

        if peca_encontrada['Quantidade: '] < quantidade:
            print('Não é possível desfazer: estoque insuficiente.')
            return

        peca_encontrada['Quantidade: '] -= quantidade

    else:
        peca_encontrada['Quantidade: '] += quantidade

    # Remove somente depois de desfazer com sucesso
    historico_movimentacoes.pop()

    print('Movimentação desfeita com sucesso!')
