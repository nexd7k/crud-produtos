#GET - Retrieve(Get) data
#POST - Write data (Write new data)
#DELETE - Delete data
#PUT - Write data (Update existent data)
#Buscar dados da classe apenas quando for precisar escrever um novo dado ou atualizar um dado existente
#Usar elementos da lista como parâmetro quando o dado para a requisição vier da URL

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Produto(BaseModel):
    nome_produto: str
    preco_produto: float


produtos = {

    1: {'Nome': 'Óculos1', 'Preço': 150.00},
    2: {'Nome': 'Óculos2', 'Preço': 150.00},
    3: {'Nome': 'Óculos3', 'Preço': 150.00},
    4: {'Nome': 'Óculos4', 'Preço': 150.00}

}

@app.get('/')
async def root():
    return {"CRUD": 'Produtos'}

@app.get('/produtos')
async def listar_produtos():
    return {'Quantidade': len(produtos), 'Produtos': produtos}

@app.get('/produtos/{id_produto}')
async def listar_produto_por_id(id_produto: int):
    return produtos[id_produto] 

@app.post('/produtos/')
async def cadastrar_produto(dados_produto: Produto):
    id_produto = max(produtos.keys(), default = 0) + 1

    produtos[id_produto] = {
        'Nome': dados_produto.nome_produto,
        'Preço': dados_produto.preco_produto
    }


    return {'message': 'Produto cadastrado com sucesso!',
            'ID do produto': id_produto,
            'Nome do produto': dados_produto.nome_produto,
            'Preço do produto': dados_produto.preco_produto,
            }

@app.delete('/produtos/{id_produto}')
async def deletar_produto(id_produto: int):
    if id_produto in produtos:
        del produtos[id_produto]
        return {'message': f'O produto cujo id {id_produto} foi deletado com sucesso!'}

    return {'message': 'Esse id não existe'}

@app.put('/produtos/')
async def atualizar_produto(dados_produto: Produto):

    if dados_produto.id_produto in produtos:
        produtos[dados_produto.id_produto] = {
        'Nome': dados_produto.nome_produto,
        'Preço': dados_produto.preco_produto,
        }

    return {'message': f'Produto de id número {dados_produto.id_produto} atualizado com sucesso!',
            'nome': f'Novo nome: {dados_produto.nome_produto}',
            'preço': f'Novo preço: {dados_produto.preco_produto}',
    }