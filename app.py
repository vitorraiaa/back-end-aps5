from flask import Flask, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@clusteraps.jnvgfjj.mongodb.net/biblioteca_db" #sempre depois da string de conexão, adicionar /nome da base de dados
mongo = PyMongo(app, tls=True, tlsAllowInvalidCertificates=True)

@app.route('/usuarios', methods=['POST'])
def post_user():
    data = request.json
    nome = data.get('nome')
    cpf = data.get('CPF')
    data_nascimento = data.get('data')

    if cpf is not None:
        usuario_duplicado = mongo.db.usuarios_aps.find_one({'CPF': cpf})
        if usuario_duplicado is not None:
            return {"erro": "CPF já cadastrado"}, 400

    if cpf == "" or nome == "" or data_nascimento == "":
        return {"erro": "CPF, nome ou data de nascimento não pode ser vazio"}, 400

    result = mongo.db.usuarios_aps.insert_one(data)
    return {
        "id": str(result.inserted_id),
            }, 201

@app.route('/usuarios/<id>', methods=['GET'])
def get_one_user(id):
    
    filtro = {'_id': ObjectId(id)} 
    projecao = {'_id':0}
    
    dado_usuario = mongo.db.usuarios_aps.find_one(filtro, projecao)

    resp={
        'usuarios': dado_usuario
    }
    
    if dado_usuario:
        return resp, 200
    
    else:
        return {"erro": "usuario não encontrado"}, 404

@app.route('/usuarios', methods=['GET'])
def get_all_users():
    
    filtro = {}
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find(filtro, projecao)

    resp={
        'usuarios': list(dados_usuarios)
    }
    return resp, 200

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/usuarios/<id>', methods=['PUT'])
def put_user(id):
    data = request.json
    nome = data.get('nome')
    cpf = data.get('CPF')
    data_nascimento = data.get('data')

    if cpf == "" or nome == "" or data_nascimento == "":
        return {"erro": "CPF, nome ou data de nascimento não pode ser vazio"}, 400

    # Buscar o usuário pelo ID
    filtro = {'_id': ObjectId(id)}
    usuario = mongo.db.usuarios_aps.find_one(filtro)

    # Verificar se o usuário existe
    if not usuario:
        return {"erro": "Usuário não encontrado"}, 404

    # Atualizar o usuário
    result = mongo.db.usuarios_aps.update_one(filtro, {'$set': data})
    return {"id": str(result.inserted_id)}, 200
    
    
@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_user(id):
    
    filtro = {'_id': ObjectId(id)} 
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find_one(filtro, projecao)
    
    if dados_usuarios:
        result = mongo.db.usuarios_aps.delete_one(filtro)
        return {"id": str(result.inserted_id)}, 200
    
    else:
        return {"erro": "usuario não encontrado"}, 404


@app.route('/bikes', methods=['POST'])
def post_bike():
    data = request.json
    marca = data.get('marca')
    modelo = data.get('modelo')
    cidade = data.get('cidade')
    status = data.get('status')

    if marca == "" or modelo == "" or cidade == "" or status == "":
        return {"erro": "marca, modelo, cidade ou status não pode ser vazio"}, 400

    if status != "disponivel" or status!='disponível' or status != "em uso":
        return {"erro": "status pode ser apenas 'disponivel' ou 'em uso'" }, 400

    result = mongo.db.bikes_aps.insert_one(data)
    return {
        "id": str(result.inserted_id),
            }, 201

@app.route('/bikes/<id>', methods=['GET'])
def get_one_bike(id):
    
    filtro = {'_id': ObjectId(id)} 
    projecao = {'_id':0}
    
    dado_bike = mongo.db.bikes_aps.find_one(filtro, projecao)

    resp={
        'bikes': dado_bike
    }
    
    if dado_bike:
        return resp, 200
    
    else:
        return {"erro": "bike não encontrada"}, 404

@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    
    filtro = {}
    projecao = {'_id':0}
    
    dados_bikes = mongo.db.bikes_aps.find(filtro, projecao)

    resp={
        'bikes': list(dados_bikes)
    }
    return resp, 200

@app.route('/bikes/<id>', methods=['PUT'])
def put_bike(id):
    data = request.json
    marca = data.get('marca')
    modelo = data.get('modelo')
    cidade = data.get('cidade')
    status = data.get('status')

    if marca == "" or modelo == "" or cidade == "" or status == "":
        return {"erro": "marca, modelo, cidade ou status não pode ser vazio"}, 400

    if status != "disponivel" or status!='disponível' or status != "em uso":
        return {"erro": "status pode ser apenas 'disponivel' ou 'em uso'" }, 400

    filtro = {'_id': ObjectId(id)}
    projecao = {'_id':0}
    dado_bike = mongo.db.bikes_aps.find_one(filtro, projecao)

    if dado_bike:
        result = mongo.db.bikes_aps.update_one(filtro, {'$set': data})
        return {"id": str(result.inserted_id)}, 200
    
    else:
        return {"erro": "bike não encontrada"}, 404
    
@app.route('/bikes/<id>', methods=['DELETE'])
def delete_bike(id):
    
    filtro = {'_id': ObjectId(id)} 
    projecao = {'_id':0}
    
    dados_bikes = mongo.db.bikes_aps.find_one(filtro, projecao)
    
    if dados_bikes:
        result = mongo.db.bikes_aps.delete_one(filtro)
        return {"id": str(result.inserted_id)}, 200
    
    else:
        return {"erro": "bike não encontrada"}, 404

if __name__ == '__main__':
    app.run(debug=True)  