import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from decimal import Decimal
from dotenv import load_dotenv
import pymongo

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da Conexão
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.livraria        # Seleciona o banco 'livraria'
livros_collection = db.livros # Seleciona a coleção 'livros'

def buscar_livros(termo="", preco_min=None, preco_max=None, categoria=None, tags=None, pagina=1, itens_por_pagina=10):
    """
    Busca livros com filtros, ordenação e paginação.
    """
    query = {}

    # 1. Filtro por Texto titulo ou descrição usando REGEX
    if termo:
        regex = {"$regex": termo, "$options": "i"} # 'i' ignora maiúsculas ou minúsculas
        query["$or"] = [
            {"titulo": regex},
            {"descricao": regex},
            {"autores": regex},  
            {"editora": regex},   
            {"categoria": regex}
        ]

    # 2. Filtro por Preço conversão para Decimal128
    if preco_min is not None or preco_max is not None:
        query["preco"] = {}
        if preco_min:
            query["preco"]["$gte"] = Decimal128(Decimal(str(preco_min)))
        if preco_max:
            query["preco"]["$lte"] = Decimal128(Decimal(str(preco_max)))

    # 3. Filtro por Categoria igualdade simples
    if categoria:
        query["categoria"] = categoria

    # 4. Filtro por Tags Usando $all para garantir que tenha todas as tags
    if tags:
        # 'tags' vem como uma lista ['aventura', 'classico']
        query["tags"] = {"$all": tags}

    # Lógica de Paginação
    # calcula quantos documentos pular skip
    pular = (pagina - 1) * itens_por_pagina

    # Realiza a busca
    # find() -> sort() -> skip() -> limit()
    cursor = livros_collection.find(query) \
        .sort("titulo", pymongo.ASCENDING) \
        .skip(pular) \
        .limit(itens_por_pagina)

    # esrou contando o total de livros para saber quantas páginas existem
    total_livros = livros_collection.count_documents(query)

    return list(cursor), total_livros

def buscar_livro_por_id(id_str):
    """
    Busca um livro específico pelo seu _id.
    """
    try:
        # converte a string recebida da URL para ObjectId
        obj_id = ObjectId(id_str)
        livro = livros_collection.find_one({"_id": obj_id}) #
        return livro
    except Exception as e:
        print(f"Erro ao buscar ID: {e}")
        return None

def obter_categorias():
    """
    Retorna uma lista de todas as categorias únicas no banco.
    """
    return livros_collection.distinct("categoria")

def obter_tags():
    """
    Retorna uma lista de todas as tags únicas no banco.
    """
    return livros_collection.distinct("tags")