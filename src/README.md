# 💻 Código Fonte - Amigão

Esta pasta contém o coração do nosso assistente financeiro, construído de forma simples e robusta para facilitar o entendimento e manutenção.

---

## 🏗️ Estrutura Atual

```text
src/
├── app.py              # Aplicação principal (Painel e Integração com IA)
└── README.md           # Estas instruções
```

## ⚙️ Sobre o Funcionamento (`app.py`)

O `app.py` orquestra três pilares principais do projeto:
1. **Carregamento de Dados Analíticos:** Os dados da pasta `/data` (JSON/CSV) são resgatados usando `Pandas` e cache do Streamlit (`@st.cache_data`).
2. **Construção de Contexto (Prompt Engineering):** Os dados reais combinados ao papel da Persona (*System Prompt*) formam a bagagem de informações da IA a cada interação. O histórico de *Chatbot* também é persistido usando o módulo `st.session_state`.
3. **Comunicação Segura:** Fazemos chamadas de requisição HTTP (`requests`) apontando diretamente para o modelo que está operando no `Ollama` localmente (*localhost:11434*), impedindo vazamento de dados bancários do mock para servidores de nuvem externos.

## ▶️ Como Rodar

Basta estar na pasta raiz do repositório (fora do diretório `src`) e rodar:

```bash
# 1. Garanta que o modelo está de pé no Ollama
# (ollama serve / ollama run qwen3.5:4b)

# 2. Inicie a tela
python -m streamlit run src/app.py
```

## ▶️ Evidência de Execução
![alt text](image.png)