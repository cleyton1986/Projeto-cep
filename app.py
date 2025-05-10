# app.py - Aplicação Flask para a API

from flask import Flask, request, jsonify, render_template
import requests
import json
import random
import time

app = Flask(__name__)

# Sistema de cache simples - em produção usaríamos Redis ou similar
cache = {}
cache_expiry = 3600  # 1 hora em segundos

@app.route('/')
def index():
    """Página inicial com formulário para consulta de CEP"""
    return render_template('index.html')

@app.route('/api/consulta-cep/<cep>', methods=['GET'])
def api_consulta_cep(cep):
    """API endpoint para consultar CEP e retornar dados otimizados"""
    # Limpar o CEP - remover caracteres não numéricos
    cep = ''.join(filter(str.isdigit, cep))

    # Validar CEP
    if len(cep) != 8:
        return jsonify({"erro": "CEP inválido. Deve conter 8 dígitos."}), 400

    # Verificar cache
    now = time.time()
    if cep in cache and now - cache[cep]['timestamp'] < cache_expiry:
        dados = cache[cep]['data']
        return jsonify({
            "dados": dados,
            "estacionamentos": encontrar_estacionamentos(dados),
            "fonte": "cache"
        })

    # Consultar a API ViaCEP
    dados = consultar_viacep(cep)

    if "erro" in dados:
        return jsonify({"erro": dados["erro"]}), 404

    # Salvar no cache
    cache[cep] = {
        'data': dados,
        'timestamp': now
    }

    # Retornar os dados filtrados e estacionamentos simulados
    return jsonify({
        "dados": dados,
        "estacionamentos": encontrar_estacionamentos(dados),
        "fonte": "api"
    })

def consultar_viacep(cep):
    """Consulta a API ViaCEP e filtra apenas os dados necessários"""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados_completos = response.json()

            # Verificar se o CEP existe
            if "erro" in dados_completos:
                return {"erro": "CEP não encontrado"}

            # Filtrar apenas os dados essenciais
            dados_filtrados = {
                "logradouro": dados_completos.get("logradouro", ""),
                "bairro": dados_completos.get("bairro", ""),
                "localidade": dados_completos.get("localidade", ""),
                "uf": dados_completos.get("uf", "")
            }
            return dados_filtrados
        else:
            return {"erro": "CEP não encontrado"}
    except Exception as e:
        return {"erro": str(e)}

def encontrar_estacionamentos(endereco):
    """
    Simula a busca de estacionamentos próximos com base no endereço
    Em uma aplicação real, consultaríamos uma API como Google Places
    """
    # Lista de nomes fictícios de estacionamentos
    nomes = [
        "Estacionamento Central",
        "Park & Go",
        "Estacione Aqui",
        "Parking 24h",
        "Vaga Fácil",
        "EstacionaBem",
        "Vaga Segura",
        "AutoPark",
        "Garagem Expressa",
        "Estacionamento Rápido"
    ]

    # Para simular diferenças por região, usamos a UF
    uf = endereco.get("uf", "SP")
    seed = sum(ord(c) for c in uf)  # Gera um número baseado nas letras da UF
    random.seed(seed + len(endereco.get("logradouro", "")))

    # Escolhe aleatoriamente 1-5 estacionamentos
    num_estacionamentos = random.randint(1, 5)
    estacionamentos_selecionados = random.sample(nomes, num_estacionamentos)

    # Cria dados aleatórios para cada estacionamento
    resultado = []
    for nome in estacionamentos_selecionados:
        resultado.append({
            "nome": nome,
            "distancia": f"{random.randint(1, 20) * 100} metros",
            "vagas_disponiveis": random.randint(0, 30),
            "preco_hora": f"R$ {random.randint(5, 20)},00"
        })

    return resultado

@app.route('/comparacao-economia')
def comparacao_economia():
    """Página que mostra a comparação de economia de dados"""
    return render_template('comparacao.html')

@app.route('/api/comparacao', methods=['GET'])
def api_comparacao():
    """API endpoint que retorna a comparação de tamanho dos dados"""
    # Exemplo de resposta completa da API ViaCEP
    exemplo_resposta_original = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107"
    }

    # Exemplo de resposta filtrada
    exemplo_resposta_filtrada = {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }

    # Calcula tamanhos
    tamanho_original = len(json.dumps(exemplo_resposta_original).encode('utf-8'))
    tamanho_filtrado = len(json.dumps(exemplo_resposta_filtrada).encode('utf-8'))

    # Calcula a economia
    economia_percentual = round((1 - tamanho_filtrado/tamanho_original) * 100, 2)

    return jsonify({
        "resposta_original": exemplo_resposta_original,
        "resposta_filtrada": exemplo_resposta_filtrada,
        "tamanho_original": tamanho_original,
        "tamanho_filtrado": tamanho_filtrado,
        "economia_percentual": economia_percentual
    })

if __name__ == '__main__':
    app.run(debug=True)