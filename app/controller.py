import json
from datetime import datetime

from flask import Blueprint, Response, request
from sqlalchemy import select

from app.model import (
    Categoria,
    Funcionario,
    Pedido,
    PedidoProduto,
    Produto,
    StatusPedido,
    db_session,
)

app = Blueprint("main_controller", __name__)

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/login', methods=['POST'])
def login():
    try:
        # Obtém os dados do login do corpo do request
        data = request.get_json()

        # Verifica se o corpo da requisição contém email e senha
        if not data or not data.get('email') or not data.get('senha'):
            return Response(
                json.dumps({'status': 'erro', 'message': 'Email e senha são obrigatórios!'}),
                status=400,
                mimetype='application/json'
            )

        email = data.get('email')
        senha = data.get('senha')

        # Verifica se o email e a senha correspondem aos dados armazenados
        if email == ADMIN_EMAIL and senha == ADMIN_PASSWORD:
            # Retorna resposta de sucesso
            response_data = {
                'status': 'sucesso',
                'message': 'Login realizado com sucesso!'
            }
            return Response(
                json.dumps(response_data),
                status=200,
                mimetype='application/json'
            )
        else:
            # Retorna resposta de erro se os dados estiverem incorretos
            response_data = {
                'status': 'erro',
                'message': 'Email ou senha incorretos!'
            }
            return Response(
                json.dumps(response_data),
                status=401,
                mimetype='application/json'
            )

    except Exception as e:
        # Caso ocorra algum erro inesperado
        return Response(
            json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/categorias', methods=['GET'])
def ListAllCategorias():
    try:
        categoria_query = select(Categoria).select_from(Categoria)
        categorias = db_session.execute(categoria_query).scalars()
        result = [categoria.serialize() for categoria in categorias]
        return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/categoria/<int:id>', methods=['GET'])
def listCategoriaById(id):
    try:
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()
        if categoria:
            return Response(
                json.dumps(categoria.serialize()),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )





@app.route('/categoria', methods=['POST'])
def createCategoria():
    try:
        # Verifica se o conteúdo da requisição é JSON
        if not request.is_json:
            return Response(
                json.dumps({'status': 'error', 'message': 'A requisição deve ser no formato JSON'}),
                status=400,
                mimetype='application/json'
            )

        categoria_data = request.get_json()

        # Validações do campo 'nome'
        if 'nome' not in categoria_data:
            return Response(
                json.dumps({'status': 'error', 'message': 'Campo "nome" é obrigatório.'}),
                status=400,
                mimetype='application/json'
            )

        nome = categoria_data['nome']

        # Verifica se o nome não está vazio e se tem no máximo 40 caracteres
        if not nome.strip():
            return Response(
                json.dumps({'status': 'error', 'message': 'O campo "nome" não pode ser vazio.'}),
                status=400,
                mimetype='application/json'
            )

        if len(nome) > 40:
            return Response(
                json.dumps({'status': 'error', 'message': 'O campo "nome" não pode ter mais de 40 caracteres.'}),
                status=400,
                mimetype='application/json'
            )

        # Cria a categoria no banco de dados
        categoria = Categoria(
            nome=nome
        )
        categoria.save()

        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Categoria registrada com sucesso!',
                'categoria': categoria.serialize()
            }),
            status=201,
            mimetype='application/json'
        )

    except Exception as e:
        # Log do erro
        print(f"Erro: {str(e)}")
        return Response(
            json.dumps({'status': 'error', 'message': f"Erro interno: {str(e)}"}),
            status=500,
            mimetype='application/json'
        )


@app.route('/categoria/<int:id>', methods=['PUT'])
def updateCategoria(id):
    try:
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()
        if not categoria:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )

        data = request.get_json()

        if 'nome' in data:
            categoria.nome = data['nome']

        categoria.save()

        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Categoria atualizada com sucesso!',
                'categoria': categoria.serialize()
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/categoria/delete/<int:id>', methods=['POST'])
def deleteCategoria(id):
    try:
        # Seleciona a categoria com base no ID
        categoria_sql = select(Categoria).where(Categoria.id == id)
        categoria = db_session.execute(categoria_sql).scalar()

        # Verifica se a categoria foi encontrada
        if not categoria:
            return Response(
                json.dumps({'status': 'error', 'message': 'Categoria não encontrada'}),
                status=404,
                mimetype='application/json'
            )

        # Exclui a categoria
        categoria.delete()

        # Retorna a resposta de sucesso
        final = {
            'status': 'success',
            'message': f'{categoria.nome} foi excluída com sucesso!'
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Caso ocorra um erro, retorna uma resposta com o erro
        final = {
            'status': 'error',
            'message': str(e)
        }
        return Response(
            response=json.dumps(final),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionarios', methods=['GET'])
def ListAllFuncionarios():
    try:
        funcionario_query = select(Funcionario).select_from(Funcionario)
        funcionarios = db_session.execute(funcionario_query).scalars()
        result = [funcionario.serialize() for funcionario in funcionarios]
        return Response(
            json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/<int:id>', methods=['GET'])
def listFuncionarioById(id):
    try:
        # Busca o funcionário pelo ID usando SQLAlchemy
        funcionario = db_session.query(Funcionario).filter(Funcionario.id == id).first()

        # Verifica se o funcionário foi encontrado
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa os dados do funcionário
        final = json.dumps(funcionario.serialize())  # Serialize o objeto diretamente
        return Response(
            response=final,
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario', methods=['POST'])
def createFuncionario():
    try:

        funcionario_data = request.get_json()
        # Criação do novo funcionário
        funcionario = Funcionario(
            nome=funcionario_data['nome'],
            email=funcionario_data['email'],
            senha=funcionario_data['senha'],
            telefone=funcionario_data['telefone']

        )
        funcionario.save()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': 'Funcionário registrado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'senha': funcionario.senha,
            'telefone': funcionario.telefone
        }

        return Response(
            response=json.dumps(final),
            status=201,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/<int:id>', methods=['PUT'])
def updateFuncionario(id):
    try:
        # Busca o funcionário
        funcionario_sql = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário existe
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        data = request.get_json()

        # Atualiza os dados do funcionário
        if 'nome' in data:
            funcionario.nome = data['nome']
        if 'email' in data:
            funcionario.email = data['email']
        if 'senha' in data:
            funcionario.senha = data['senha']
        if 'telefone' in data:
            funcionario.telefone = data['telefone']

        funcionario.save()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': 'Funcionário atualizado com sucesso!',
            'nome': funcionario.nome,
            'email': funcionario.email,
            'senha': funcionario.senha,
            'telefone': funcionario.telefone
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/delete/<int:id>', methods=['POST'])
def deleteFuncionario(id):
    try:
        # Busca o funcionário
        funcionario_sql = select(Funcionario).where(Funcionario.id == id)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário foi encontrado
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Exclui o funcionário
        funcionario.delete()

        # Resposta de sucesso
        final = {
            'status': 'success',
            'message': f'{funcionario.nome} foi excluído com sucesso!'
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/funcionario/login', methods=['POST'])
def loginFuncionario():
    try:
        # Recebe os dados enviados na requisição (email e senha)
        email = request.json.get('email')
        senha = request.json.get('senha')

        # Verifica se o email e senha foram informados
        if not email or not senha:
            return Response(
                json.dumps({'status': 'error', 'message': 'Email e senha são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Consulta o funcionário pelo email
        funcionario_sql = select(Funcionario).where(Funcionario.email == email)
        funcionario = db_session.execute(funcionario_sql).scalar()

        # Verifica se o funcionário existe
        if not funcionario:
            return Response(
                json.dumps({'status': 'error', 'message': 'Funcionário não encontrado'}),
                status=404,
                mimetype='application/json'
            )

            # Verificar a senha
        if funcionario.senha != senha:
            return Response(
                response=json.dumps({'status': 'error', 'message': 'Invalid credentials'}),
                status=401,
                mimetype='application/json'
            )

        # Se o login for bem-sucedido, retorna os dados do funcionário e o token
        final = {
            'status': 'success',
            'message': 'Login bem-sucedido',
            'funcionario': funcionario.serialize()
        }

        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Se houver qualquer erro, retorna uma resposta com o erro
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/produtos', methods=['GET'])
def ListAllProdutos():
    try:
        produto_query = select(Produto).select_from(Produto)
        produtos = db_session.execute(produto_query).scalars().all()  # Use .scalars().all() para obter todos os resultados

        result = [produto.serialize() for produto in produtos]  # Itera sobre os produtos retornados

        return Response(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produto/<int:id>', methods=['GET'])
def listProdutoById(id):
    try:
        # Consulta o produto pelo ID
        produto_sql = select(Produto).where(Produto.id == id)
        produto_result = db_session.execute(produto_sql).fetchone()

        # Verifica se o produto existe
        if not produto_result:
            return Response(
                json.dumps({'status': 'error', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        produto = produto_result[0]

        # Serializa o produto
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto encontrado',
                'id': produto.id,
                'nome': produto.nome,
                'preco': produto.preco,
                'descricao': produto.descricao,
                'image': produto.imagem,
                'categoria_id': produto.categoria_id
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna uma resposta de erro genérica
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao buscar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )

@app.route('/produto', methods=['POST'])
def createProduto():
    try:
        # Lê os dados JSON da requisição
        data = request.get_json()

        # Verifica se todos os campos obrigatórios estão presentes
        if not data or not data.get('nome') or not data.get('preco') or not data.get('descricao') or not data.get('imagem') or not data.get('categoria_id'):
            return Response(
                json.dumps({'status': 'error', 'message': 'Todos os campos são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Cria o novo produto
        produto = Produto(
            nome=data['nome'],
            descricao=data['descricao'],
            imagem=data['imagem'],
            preco=data['preco'],
            categoria_id=data['categoria_id']
        )
        produto.save()  # Salva o produto no banco de dados

        # Retorna sucesso
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto registrado com sucesso!',
                'produto': produto.serialize()
            }),
            status=201,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna erro genérico
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao criar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )


@app.route('/produto/<int:id>', methods=['PUT'])
def updateProduto(id):
    try:
        # Consulta o produto pelo ID
        produto_sql = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto_sql).scalar()

        # Verifica se o produto existe
        if not produto:
            return Response(
                json.dumps({'status': 'error', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        data = request.get_json()

        # Atualiza os campos, caso sejam informados
        if 'nome' in data:
            produto.nome = data['nome']
        if 'descricao' in data:
            produto.descricao = data['descricao']
        if 'imagem' in data:
            produto.imagem = data['imagem']
        if 'preco' in data:
            produto.preco = data['preco']
        if 'categoria_id' in data:
            produto.categoria_id = data['categoria_id']

        # Salva as alterações
        produto.save()

        # Retorna sucesso
        return Response(
            json.dumps({
                'status': 'success',
                'message': 'Produto atualizado com sucesso!',
                'produto': produto.serialize()
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        # Retorna erro genérico
        return Response(
            json.dumps({'status': 'error', 'message': f'Erro ao atualizar produto: {str(e)}'}),
            status=500,
            mimetype='application/json'
        )

@app.route('/produto/delete/<int:id>', methods=['POST'])
def deleteProduto(id):
    try:
        # Verifica se o produto existe
        produto_sql = select(Produto).where(Produto.id == id)
        produto = db_session.execute(produto_sql).scalar()

        # Se o produto não for encontrado, retorna um erro
        if not produto:
            return Response(
                response=json.dumps({
                    'status': 'error',
                    'message': f'Produto com ID {id} não encontrado.'
                }),
                status=404,
                mimetype='application/json'
            )

        # Deleta o produto
        produto.delete()

        # Retorna resposta de sucesso após exclusão
        final = {
            'status': 'success',
            'message': f'O produto "{produto.nome}" foi excluído com sucesso.'
        }
        return Response(
            response=json.dumps(final),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        # Trata exceções e retorna mensagem de erro
        return Response(
            response=json.dumps({
                'status': 'error',
                'message': f'Erro ao excluir o produto: {str(e)}'
            }),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido/<int:pedido_id>', methods=['GET'])
def listPedidoById(pedido_id):
    try:
        # Buscar o pedido pelo ID, incluindo os produtos associados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()

        # Verificar se o pedido existe
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Buscar os produtos associados ao pedido
        produtos = db_session.query(PedidoProduto).filter(PedidoProduto.pedido_id == pedido_id).all()

        # Serializar os produtos
        produtos_serializados = [produto.serialize() for produto in produtos]

        # Retornar o pedido com os produtos
        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'pedido': pedido.serialize(),
                'produtos': produtos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedidos/status/<string:status>', methods=['GET'])
def listarPedidosByStatus(status):
    try:
        # Verifica se o status é válido
        valid_status = ['PENDENTE', 'EM_ESPERA', 'EM_PRODUCAO', 'FINALIZADO']
        if status not in valid_status:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Status inválido. Valores permitidos: {", ".join(valid_status)}'}),
                status=400,
                mimetype='application/json'
            )

        # 1. Busca todos os pedidos que têm o status especificado
        pedidos = db_session.query(Pedido).filter(Pedido.status == status).all()

        # Verifica se não encontrou pedidos
        if not pedidos:
            return Response(
                response=json.dumps({'status': 'erro', 'message': f'Não há pedidos com o status {status}'}),
                status=404,
                mimetype='application/json'
            )

        # Serializa os pedidos
        pedidos_serializados = [pedido.serialize() for pedido in pedidos]

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'pedidos': pedidos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido/produtos/<int:pedido_id>', methods=['GET'])
def listAllProdutoByPedido(pedido_id):
    try:
        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Busca todos os produtos associados ao pedido através da tabela PedidoProduto
        produtos_do_pedido = db_session.query(Produto, PedidoProduto.quantidade).join(PedidoProduto).filter(PedidoProduto.pedido_id == pedido_id).all()

        # Verifica se existem produtos associados ao pedido
        if not produtos_do_pedido:
            return Response(
                response=json.dumps({'status': 'sucesso', 'message': 'Nenhum produto associado a este pedido'}),
                status=200,
                mimetype='application/json'
            )

        # Serializa os produtos e retorna como resposta, incluindo a quantidade dentro do produto
        produtos_serializados = [
            {
                **produto.serialize(),  # Inclui todos os dados do produto
                'quantidade': quantidade  # Adiciona a quantidade do produto
            }
            for produto, quantidade in produtos_do_pedido
        ]

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Produtos associados ao pedido recuperados com sucesso',
                'pedido': pedido.serialize(),
                'produtos': produtos_serializados
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

@app.route('/pedido', methods=['POST'])
def criarPedido():
    try:
        # Use request.get_json() para obter os dados enviados como JSON
        data = request.get_json()

        mesa = data.get('mesa')
        funcionario_id = data.get('funcionario_id')

        if not mesa or not funcionario_id:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Mesa e funcionario_id são obrigatórios'}),
                status=400,
                mimetype='application/json'
            )

        # Criar pedido sem status e dataCriado
        pedido = Pedido(
            mesa=mesa,
            status=StatusPedido.PENDENTE,  # Status temporário ou 'pendente' até a finalização
            funcionario_id=int(funcionario_id),
        )

        db_session.add(pedido)
        db_session.commit()  # O pedido é persistido no banco de dados, mas sem status definitivo.

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Pedido criado com sucesso!',
                'pedido': pedido.serialize()  # Retorna o pedido criado
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )

VALID_STATUSES = ['PENDENTE', 'EM_ESPERA', 'EM_PRODUCAO', 'FINALIZADO']

@app.route('/pedido/update-status/<int:pedido_id>', methods=['PUT'])
def updatePedido(pedido_id):
    try:
        # Pega o JSON enviado na requisição
        data = request.get_json()

        status = data.get('status')  # Agora obtemos o status do JSON

        if not status or status not in VALID_STATUSES:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Status inválido. Valores permitidos: PENDENTE, EM_ESPERA, EM_PRODUCAO, FINALIZADO'}),
                status=400,
                mimetype='application/json'
            )

        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()

        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Atualiza o status do pedido
        pedido.status = status
        db_session.commit()

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Status do pedido atualizado com sucesso!',
                'pedido': pedido.serialize()
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/pedido/adicionar-produto', methods=['POST'])
def adicionarProduto():
    try:
        # Pega os dados do JSON enviado na requisição
        data = request.get_json()

        pedido_id = data.get('pedido_id')
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade')

        # Verifica se todos os dados obrigatórios foram passados
        if not pedido_id or not produto_id or not quantidade:
            return Response(
                response=json.dumps(
                    {'status': 'erro', 'message': 'Pedido ID, Produto ID e Quantidade são obrigatórios'}
                ),
                status=400,
                mimetype='application/json'
            )

        # Busca o pedido no banco de dados
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Busca o produto no banco de dados
        produto = db_session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Produto não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Verifica se o produto já foi adicionado ao pedido
        pedido_produto = db_session.query(PedidoProduto).filter_by(pedido_id=pedido.id, produto_id=produto.id).first()
        if pedido_produto:
            # Se já existe, atualiza a quantidade
            pedido_produto.quantidade += int(quantidade)
        else:
            # Caso contrário, cria uma nova associação
            pedido_produto = PedidoProduto(
                pedido_id=int(pedido.id),
                produto_id=int(produto.id),
                quantidade=int(quantidade)
            )
            db_session.add(pedido_produto)

        db_session.commit()  # Salva a associação no banco de dados

        # Busca os produtos relacionados ao pedido com a quantidade
        produtos_do_pedido = db_session.query(PedidoProduto, Produto).join(Produto).filter(PedidoProduto.pedido_id == pedido.id).all()

        # Formata os produtos para incluir a quantidade
        produtos_com_quantidade = [
            {
                'id': produto.id,
                'nome': produto.nome,
                'preco': produto.preco,
                'quantidade': pedido_produto.quantidade
            } for pedido_produto, produto in produtos_do_pedido
        ]

        # Retorna a resposta com o pedido e seus produtos atualizados
        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Produto adicionado ao pedido!',
                'pedido': pedido.serialize(),  # Retorna o pedido atualizado
                'produtos': produtos_com_quantidade  # Retorna os produtos com quantidade
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/pedido/finalizar', methods=['POST'])
def finalizarPedido():
    try:
        # Pega os dados do JSON enviado na requisição
        data = request.get_json()
        pedido_id = data.get('pedido_id')  # O pedido a ser finalizado

        if not pedido_id:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido ID é obrigatório'}),
                status=400,
                mimetype='application/json'
            )

        # Buscar o pedido pelo ID
        pedido = db_session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não encontrado'}),
                status=404,
                mimetype='application/json'
            )

        # Verificar se o pedido tem pelo menos um produto associado
        produtos_associados = db_session.query(PedidoProduto).filter_by(pedido_id=pedido_id).all()
        if not produtos_associados:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Pedido não pode ser finalizado sem produtos'}),
                status=400,
                mimetype='application/json'
            )

        # Atualizar o status do pedido para "EM_ESPERA" e adicionar a data de criação
        pedido.status = StatusPedido.EM_ESPERA
        pedido.dataCriado = datetime.now()  # Atribui a data atual
        db_session.commit()  # Commit para salvar as alterações

        return Response(
            response=json.dumps({
                'status': 'sucesso',
                'message': 'Pedido finalizado com sucesso!',
                'pedido': pedido.serialize()
            }),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )


@app.route('/pedido/<int:pedido_id>/produto/<int:produto_id>', methods=['POST'])
def removerProduto(pedido_id, produto_id):
    try:
        # Busca a associação entre pedido e produto
        pedido_produto = db_session.query(PedidoProduto).filter_by(pedido_id=pedido_id, produto_id=produto_id).first()

        if not pedido_produto:
            return Response(
                response=json.dumps({'status': 'erro', 'message': 'Produto não encontrado no pedido'}),
                status=404,
                mimetype='application/json'
            )

        # Remove a associação do produto com o pedido
        db_session.delete(pedido_produto)
        db_session.commit()

        return Response(
            response=json.dumps({'status': 'sucesso', 'message': 'Produto removido do pedido'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': 'erro', 'message': str(e)}),
            status=500,
            mimetype='application/json'
        )
