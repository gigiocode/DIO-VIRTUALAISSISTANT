import json
import pandas as pd
import requests
import streamlit as st
import os

# ========== CONFIGURAÇÃO ==========
OLLAMA_URL = "http://localhost:11434/api/generate"
# Você pode alterar o modelo abaixo para o seu modelo local do Ollama (ex: "llama3", "mistral", etc.)
MODELO = "qwen3.5:4b" 

# Configurando caminhos para garantir que encontre a pasta "data" não importa de onde execute
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ========== CARREGAR DADOS ==========
@st.cache_data
def carregar_dados():
    """
    Função com cache (melhor prática Streamlit) para ler as bases do cliente somente uma vez.
    Adicionado tratamento de erros para ajudar na depuração.
    """
    try:
        perfil = json.load(open(os.path.join(DATA_DIR, 'perfil_investidor.json'), encoding='utf-8'))
        produtos = json.load(open(os.path.join(DATA_DIR, 'produtos_financeiros.json'), encoding='utf-8'))
        transacoes = pd.read_csv(os.path.join(DATA_DIR, 'transacoes.csv'))
        # historico = pd.read_csv(os.path.join(DATA_DIR, 'historico_atendimento.csv'))
        return perfil, produtos, transacoes
    except Exception as e:
        st.error(f"Erro ao carregar os dados. Verifique a estrutura da pasta 'data'. Detalhes: {e}")
        return {}, {}, pd.DataFrame()

perfil, produtos, transacoes = carregar_dados()

# ========== MONTAR CONTEXTO ==========
# Formatar a tabela de transações garantindo estabilidade
transacoes_str = transacoes.to_string(index=False) if not transacoes.empty else "Nenhuma transação na base."
produtos_str = json.dumps(produtos, indent=2, ensure_ascii=False) if produtos else "Nenhum produto."

contexto = f"""
CLIENTE: {perfil.get('nome', 'Cliente')}, {perfil.get('idade', 'N/A')} anos, perfil {perfil.get('perfil_investidor', 'indefinido')}
OBJETIVO: {perfil.get('objetivo_principal', 'Não definido')}
PATRIMÔNIO: R$ {perfil.get('patrimonio_total', 0)} | RESERVA: R$ {perfil.get('reserva_emergencia_atual', 0)}

TRANSAÇÕES RECENTES:
{transacoes_str}

PRODUTOS DISPONÍVEIS:
{produtos_str}
"""

# ========== SYSTEM PROMPT ==========
# Prompt já adaptado com a sua Persona documentada e lapidada
SYSTEM_PROMPT = """Você é o Amigão, um agente financeiro inteligente, consultivo e direto, conectado para ajudar o usuário a economizar, construir reserva de emergência e começar a investir.

PERSONALIDADE:
Engraçado, pessoal, direto e extremamente didático. Você julga, de forma cômica e irônica, os gastos impensados dos clientes.
Você chama homens de "amigão" e mulheres de "amigona". Seu tom é informal e acessível.

REGRAS:
1. Nunca dê recomendações de investimento se o perfil do cliente não estiver definido. Em vez disso, eduque-o sobre a necessidade de ter um perfil.
2. Identifique nas transações os gastos desnecessários e faça comentários julgadores construtivos, recomendando sempre tentar poupar pelo menos 20% do salário.
3. Se perguntado sobre assuntos não financeiros, recuse educadamente usando o estilo "amigão", dizendo que só manja de dinheiro.
4. Explique os termos difíceis de renda fixa e diversificação de maneira informal, como se estivesse conversando num bar ou tomando um café.
"""

# ========== CHAMAR OLLAMA ==========
def perguntar(msg, historico_chat):
    # Embeber as últimas interações no prompt para o LLM não perder o contexto da conversa
    historico_str = "\n".join([f"{'Usuário' if m['role'] == 'user' else 'Amigão'}: {m['content']}" for m in historico_chat[-4:]])
    
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

HISTÓRICO DA CONVERSA:
{historico_str}

Usuário: {msg}
Amigão:"""

    try:
        r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
        r.raise_for_status()
        return r.json().get('response', 'Tive um problema na resposta do sistema central.')
    except requests.exceptions.RequestException as e:
        return f"Vish amigão, a conexão com o Ollama falhou. Confere se o serviço tá rodando no {OLLAMA_URL}. Erro: {e}"

# ========== INTERFACE STREAMLIT ==========
st.set_page_config(page_title="Amigão - Seu Conselheiro", page_icon="💸", layout="centered")
st.title("💸 Amigão, o Conselheiro Financeiro")
st.caption("O robô financista que te diz as verdades na cara")

# Mantém o histórico no session state para não sumir o chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário (UI)
if pergunta := st.chat_input("Fala amigão, manda aqui a sua dúvida..."):
    # Mensagem do user na tela e salva estado
    st.chat_message("user").write(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})
    
    # Processa e recupera resposta via Ollama
    with st.spinner("Puxando o histórico para não falar besteira..."):
        resposta = perguntar(pergunta, st.session_state.messages)
        
    # Anexa e exibe resposta do agente
    st.chat_message("assistant").write(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
