import os
import json
import yaml
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def carregar_especificacao(caminho_arquivo):
    """Lê o arquivo YAML/JSON do Swagger/OpenAPI."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def gerar_mock_gemini(client, path, method, spec_endpoint):
    """Envia a especificação do endpoint para o Gemini gerar um JSON de mock."""
    print(f"🤖 Solicitando mock para {method.upper()} {path} ao Gemini...")
    
    prompt = f"""
    Você é um desenvolvedor backend sênior especialista em criação de mocks para testes.
    Abaixo está a especificação OpenAPI de um endpoint específico.
    
    Endpoint: {path}
    Método HTTP: {method.upper()}
    Especificação:
    {json.dumps(spec_endpoint, indent=2, ensure_ascii=False)}

    Sua tarefa:
    Gere um mock de resposta realista e criativo em formato JSON para o caso de sucesso (HTTP 200/201).
    Preencha os campos com dados fictícios plausíveis (nomes reais, emails válidos, datas recentes, etc).
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7 # Um pouco de criatividade para gerar dados diferentes a cada execução
        )
    )
    
    return response.text

def main():
    parser = argparse.ArgumentParser(description="Gera Mocks JSON a partir de um OpenAPI usando Gemini.")
    parser.add_argument("--spec", default="api_spec.yaml", help="Caminho para o arquivo YAML/JSON do OpenAPI")
    parser.add_argument("--path", required=True, help="O path da API que você quer mockar (ex: /usuarios/{id})")
    parser.add_argument("--method", default="get", help="O método HTTP (get, post, put, etc)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERRO: A variável de ambiente GEMINI_API_KEY não está configurada.")
        return

    client = genai.Client(api_key=api_key)

    try:
        spec = carregar_especificacao(args.spec)
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo {args.spec} não encontrado.")
        return

    # 3. Validar se a rota existe no arquivo
    endpoint_data = spec.get("paths", {}).get(args.path, {}).get(args.method.lower())
    if not endpoint_data:
        print(f"❌ ERRO: Rota '{args.method.upper()} {args.path}' não encontrada no arquivo {args.spec}.")
        return

    mock_json_str = gerar_mock_gemini(client, args.path, args.method, endpoint_data)


    nome_arquivo_saida = f"mock_{args.method.lower()}_{args.path.replace('/', '_').replace('{', '').replace('}', '')}.json"
    
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
        mock_dit = json.loads(mock_json_str)
        json.dump(mock_dit, f, indent=4, ensure_ascii=False)

    print(f"✅ Mock gerado com sucesso! Arquivo salvo como: {nome_arquivo_saida}")

if __name__ == "__main__":
    main()