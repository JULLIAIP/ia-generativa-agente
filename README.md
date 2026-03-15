# Gerador de Mocks de API com IA Generativa (Gemini)

Este projeto é uma ferramenta de linha de comando (CLI) construída em Python que utiliza a Inteligência Artificial Generativa do Google (modelo Gemini 2.5 Flash) para ler especificações de API (OpenAPI/Swagger) e gerar automaticamente arquivos `.json` com mocks realistas.

Isso permite que times de Front-end iniciem o desenvolvimento e os testes antes mesmo de o Back-end estar pronto, eliminando gargalos no ciclo de desenvolvimento de software.

---

## Pré-requisitos

- Python 3.8 ou superior instalado.
- Uma chave de API válida do Google Gemini (`GEMINI_API_KEY`).

---

##  Como Instalar e Configurar

1. **Clone ou baixe este repositório.**
2. **Instale as dependências** executando o comando abaixo no terminal:
   ```bash
   pip install -r requirements.txt
3. **Configure sua chave de API:**

- No Mac/Linux: export GEMINI_API_KEY="sua_chave_aqui"
- No Windows (PowerShell): $env:GEMINI_API_KEY="sua_chave_aqui"
- Alternativa: Você pode criar um arquivo .env na raiz do projeto contendo GEMINI_API_KEY="sua_chave_aqui".

--- 

## Rotas Possíveis
O script é dinâmico e lê as rotas diretamente do arquivo api_spec.yaml.
Rotas configuradas atualmente no YAML de exemplo:
GET /usuarios/{id} : Retorna os detalhes de um usuário específico (gera id, nome, email, data de cadastro e status).

#### 💡 Como adicionar mais rotas?
Basta abrir o arquivo api_spec.yaml e adicionar novos caminhos sob a chave paths. Por exemplo, você pode adicionar um POST /usuarios ou um GET /produtos. O script entenderá automaticamente qualquer nova rota validada no YAML!

---

## Como Usar
Para gerar um mock, execute o script gerador_mocks.py passando o caminho (--path) e o método HTTP (--method) desejados.
Comando de exemplo: python gerador_mocks.py --path "/usuarios/{id}" --method "get" 
#### (Se estiver usando Mac e o comando acima falhar, utilize python3 no lugar de python).

### O que acontece em seguida?
O script enviará o escopo exato dessa rota para o Gemini. A IA entenderá os tipos de dados necessários e criará um arquivo JSON na sua pasta com dados fictícios realistas.
Exemplo de saída (mock_get__usuarios_id.json):

{
    "id": "123",
    "nome": "Carlos Eduardo Figueiredo",
    "email": "carlos.figueiredo@emailfalso.com.br",
    "data_cadastro": "2023-10-27T14:32:00Z",
    "ativo": true
}
