from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@progeficaz.sdiyyto.mongodb.net/biblioteca_db" #sempre depois da string de conexão, adicionar /nome da base de dados
mongo = PyMongo(app, tls=True, tlsAllowInvalidCertificates=True)

@app.route('/usuarios', methods=['POST'])
def post_user():
    
    data = request.json
    filtro = {}
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find(filtro, projecao)
    if "cpf" in dados_usuarios:
        return {"erro": "este cpf ja está cadastrado"}, 400
    if "cpf" == ' ':
        return {"erro": "cpf é obrigatório"}, 400
    
    result = mongo.db.usuarios_aps.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/usuarios/<id>', methods=['GET'])
def get_one_user(id):
    
    filtro = {'id': id}
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find_one(filtro, projecao)

    resp={
        'usuarios': list(dados_usuarios)
    }
    
    if dados_usuarios:
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
    filtro = {'id': id}
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find_one(filtro, projecao)
    
    if dados_usuarios:
        result = mongo.db.usuarios_aps.update_one(filtro, {'$set': data})
        return {"id": str(result.inserted_id)}, 200
    
    else:
        return {"erro": "usuario não encontrado"}, 404
    
    
@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_user(id):
    
    filtro = {'id': id}
    projecao = {'_id':0}
    
    dados_usuarios = mongo.db.usuarios_aps.find_one(filtro, projecao)
    
    if dados_usuarios:
        result = mongo.db.usuarios_aps.delete_one(filtro)
        return {"id": str(result.inserted_id)}, 200
    
    else:
        return {"erro": "usuario não encontrado"}, 404