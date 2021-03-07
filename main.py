import matplotlib.pyplot as plt
import pymysql.cursors

connect = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autentico = False

def logarCadastrar(decisao):
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu usuário: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            print('Usuário e/ou senha incorreto!')

    elif decisao == 2:
        print('Faça seu cadastro:')
        nome = input('Digite o nome de usuário: ')
        senha = input('Digite a senha do usuário: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('Usuário e/ou senha existente! Tente um nome ou senha diferente.')
        elif usuarioExistente == 0:
            try:
                with connect.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome,senha,nivel) values(%s,%s,%s)',(nome,senha,1))
                    connect.commit()
                    print("Usuário cadastrado com sucesso !")
            except:
                print("Erro ao inserir os dados !")

    return autenticado, usuarioMaster

def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente a esse produto: ')
    preco = float(input('Digite o preço do produto: '))

    try:
        with connect.cursor() as cursor:
            cursor.execute('insert into produtos(nome,ingredientes,grupo,preco) values(%s,%s,%s,%s);', (nome, ingredientes, grupo, preco))
            connect.commit()
            print('Produto cadastrado com sucesso!')
    except:
        print('Erro ao cadastrar produto.')

def listarProdutos():
    produtos = []

    try:
        with connect.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao listar produtos.')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto cadastrado.')

def excluirProdutos():
    idDeletar = int(input('Digite o ID do produto que deseja deletar: '))

    try:
        with connect.cursor() as cursor:
            cursor.execute('delete from produtos where id={}'.format(idDeletar))
    except:
        print('Erro ao excluir produto')

def listarPedidos():
    pedidos = []

    decision = 0

    while decision != 2:
        pedidos.clear()

        try:
            with connect.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro ao listar pedidos')

        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Não há pedidos realizados.')

        decision = int(input('Digite 1 para dar um produto como entregue | Digite 2 para voltar'))

        if decision == 1:
            idDeletar = int(input('Digite o ID do pedido entregue '))

            try:
                with connect.cursor() as cursor:
                    cursor.execute('delete from pedidos where id={}'.format(idDeletar))
                    print('Produto dado como entregue.')
            except:
                print('Erro ao dar pedido como entregue')

def gerarEstatistica():
    nomeProdutos = []
    nomeProdutos.clear()

    grupoProdutos = []
    grupoProdutos.clear()

    try:
        with connect.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro ao fazer a consulta no banco de dados')

    try:
        with connect.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('Erro ao fazer a consulta no banco de dados')

    estado = int(input('Digite 0 para sair | 1 para pesquisar por nome | 2 para pesquisar por grupo: '))

    if estado == 1:
        decisao3 = int(input('Digite 1 para pesquisar por capital | 2 por quantidade unitária: '))
        if decisao3 == 1:

            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()
            for h in range(0, len(produtos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('Quantidade vendida em reais')
            plt.xlabel('Produtos')
            plt.show()

        if decisao3 == 2:

            try:
                with connect.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta ao banco de dados')

            try:
                with connect.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta ao banco de dados')

            grupoUnico = []
            grupoUnico.clear()

            for i in grupo:
                grupoUnico.append(i['nome'])

            grupoUnico = sorted(set(grupoUnico))
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('Quantidade unitária vendida')
            plt.xlabel('Produtos')
            plt.show()

    elif estado == 2:
        decisao3 = int(input('Digite 1 para pesquisar por capital | 2 por quantidade unitária: '))

        if decisao3 == 1:
            for i in produtos:
                grupoProdutos.append(i['grupo'])

            valores = []
            valores.clear()
            for h in range(0, len(produtos)):
                somaValor = -1
                for i in vendido:
                    if i['grupo'] == grupoProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(grupoProdutos, valores)
            plt.ylabel('Quantidade vendida em reais')
            plt.xlabel('Produtos')
            plt.show()
        if decisao3 == 2:
            try:
                with connect.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta ao banco de dados')

            try:
                with connect.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta ao banco de dados')

            grupoUnico = []
            grupoUnico.clear()

            for i in grupo:
                grupoUnico.append(i['grupo'])

            grupoUnico = sorted(set(grupoUnico))
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('Quantidade unitária vendida')
            plt.xlabel('Produtos')
            plt.show()


while not autentico:
    decisao = int(input('Digite "1" para logar | Digite "2" para Cadastrar: '))

    try:
        with connect.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar no banco de dados')

    autentico,usuarioSupremo = logarCadastrar(decisao)

if autentico == True:
    print('Usuário autenticado.')
    decisaoUsuario = 1

    if usuarioSupremo == True:
         while decisaoUsuario != 0:
            decisaoUsuario = int(input('Digite 0 para sair | 1 para cadastrar produtos | 2 para listar produtos cadastrados | 3 para excluir produtos cadastrados | 4 para listar os pedidos | 5 para gerar estatística: '))

            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()
            elif decisaoUsuario == 3:
                listarProdutos()
                excluirProdutos()
            elif decisaoUsuario == 4:
                listarPedidos()
            elif decisaoUsuario == 5:
                gerarEstatistica()
    else:
        while decisaoUsuario!= 0:
            decisaoUsuario = int(input('Digite 0 para sair | Digite 1 para listar produtos cadastrados: '))
            if decisaoUsuario == 1:
                listarProdutos()
