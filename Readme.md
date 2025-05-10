# Instruções para Executar a Aplicação de Busca de Estacionamentos por CEP

Esta aplicação é uma demonstração do projeto de intervenção para a situação-problema 3, onde desenvolvemos uma API intermediária que consome a API ViaCEP, filtra apenas os dados essenciais e simula a localização de estacionamentos próximos.

## Estrutura do Projeto

O projeto consiste em:

1. `app.py` - O arquivo principal com a aplicação Flask
2. `templates/` - Diretório com os templates HTML:
   - `index.html` - Página inicial com formulário para consulta de CEP
   - `comparacao.html` - Página que demonstra a economia de dados

## Requisitos

- Python 3.6 ou superior
- Flask (`pip install flask`)
- Requests (`pip install requests`)

## Como Executar

1. Crie a estrutura de diretórios:

   ```
   projeto-cep/
   ├── app.py
   └── templates/
       ├── index.html
       └── comparacao.html
   ```

2. Copie o código do arquivo `app.py` e dos templates para os respectivos arquivos.

3. Instale as dependências:

   ```
   pip install flask requests
   ```

4. Execute a aplicação:

   ```
   python app.py
   ```

5. Acesse a aplicação em seu navegador:
   ```
   http://127.0.0.1:5000/
   ```

## Funcionalidades Implementadas

1. **Consulta de CEP Otimizada**:

   - Consome a API ViaCEP
   - Filtra apenas os dados essenciais (logradouro, bairro, cidade e UF)
   - Reduz o tamanho da resposta em aproximadamente 55%

2. **Sistema de Cache**:

   - Armazena consultas recentes em memória
   - Expira o cache após 1 hora
   - Evita consultas repetidas à API externa

3. **Simulação de Estacionamentos**:

   - Gera aleatoriamente estacionamentos próximos
   - Inclui informações como distância, vagas disponíveis e preço/hora

4. **Demonstração de Economia de Dados**:
   - Página de comparação mostrando o JSON original e o otimizado
   - Exibe estatísticas sobre a redução no tamanho dos dados

## Possíveis Melhorias para um Sistema Real

1. Integração com uma API de geolocalização real (como Google Maps Places)
2. Implementação de um sistema de cache persistente (Redis, Memcached)
3. Adição de filtros para os estacionamentos (preço, distância, etc.)
4. Autenticação para proteger a API
5. Monitoramento e limite de requisições (rate limiting)

## Relação com o Projeto de Intervenção

Esta aplicação demonstra os conceitos apresentados no projeto de intervenção para a situação-problema 3:

- Consumo de API externa (ViaCEP)
- Filtragem de dados para otimização
- Implementação de cache para melhorar performance
- Intermediação entre o aplicativo cliente e as APIs externas

A aplicação serve como prova de conceito da solução proposta, mostrando como uma camada intermediária pode significativamente reduzir o consumo de dados e melhorar a experiência do usuário.
