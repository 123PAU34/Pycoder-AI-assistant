#from dotenv import load_dotenv
import os

import streamlit as st
from groq import Groq


# Carrega as variáveis do arquivo .env 

#load_dotenv()


# Configuração da página
st.set_page_config(
    page_title="PYCODER",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Prompt do sistema
CUSTOM_PROMPT = """
Você é o "PYCoder", um assistente de IA especialista em programação,
com foco principal em Python.

Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação
de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:

1. Foco em Programação:
Responda apenas a perguntas relacionadas a programação, algoritmos,
estruturas de dados, bibliotecas e frameworks.

2. Estrutura da Resposta:
Sempre formate suas respostas da seguinte maneira:

- Explicação Clara:
Comece com uma explicação conceitual sobre o tópico perguntado.

- Exemplo de Código:
Forneça um ou mais blocos de código em Python com sintaxe correta.

- Detalhes do Código:
Após o bloco de código, explique o que cada parte do código faz.

- Documentação de Referência:
Ao final, inclua uma seção chamada
"📚 Documentação de Referência" com um link relevante
para a documentação oficial.

3. Clareza e Precisão:
Use uma linguagem clara, didática e tecnicamente precisa.
"""


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.title("🤖 PYCoder")

    st.markdown(
        "Um assistente de IA com foco em programação Python "
        "para ajudar iniciantes."
    )

    # Pega a API Key do arquivo .env
    groq_api_key = os.getenv("GROQ_API_KEY")

    # Caso não exista no .env, permite inserir manualmente
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Digite sua API Key da Groq",
            type="password",
            help="Gere sua chave em https://console.groq.com/keys"
        )

    st.markdown("---")

    st.markdown(
        "Desenvolvido para auxiliar em dúvidas de programação Python."
    )

    st.markdown("---")

    st.link_button(
        "✉️ E-mail para suporte",
        "mailto:digiteoemailquevoceutilizara"
    )


# =========================================================
# TÍTULO
# =========================================================

st.title("Python Coder - PYCoder")

st.subheader("Assistente pessoal de programação Python 🐍")

st.caption(
    "Mande sua pergunta sobre Python e obtenha "
    "código, explicações e referências."
)


# =========================================================
# HISTÓRICO DO CHAT
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# Mostra mensagens anteriores
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# CLIENTE GROQ
# =========================================================

client = None

if groq_api_key:

    try:

        client = Groq(api_key=groq_api_key)

    except Exception as e:

        st.sidebar.error(
            f"Erro ao inicializar o cliente Groq: {e}"
        )

        st.stop()


elif st.session_state.messages:

    st.warning(
        "Por favor, insira sua API Key da Groq na barra lateral."
    )


# =========================================================
# CHAT
# =========================================================

if prompt := st.chat_input("Qual sua dúvida de Python hoje?"):

    # Verifica se existe cliente
    if not client:

        st.warning(
            "Por favor, insira sua API Key da Groq "
            "na barra lateral para continuar."
        )

        st.stop()


    # Adiciona mensagem do usuário
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # Mostra mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)


    # Monta as mensagens para enviar para a API
    messages_for_api = [
        {
            "role": "system",
            "content": CUSTOM_PROMPT
        }
    ] + st.session_state.messages


    # =====================================================
    # RESPOSTA DA IA
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner("Analisando sua pergunta..."):

            try:

                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048
                )


                # Extrai resposta
                pycoder_ai_resposta = (
                    chat_completion.choices[0].message.content
                )


                # Exibe resposta
                st.markdown(pycoder_ai_resposta)


                # Salva resposta no histórico
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": pycoder_ai_resposta
                    }
                )


            except Exception as e:

                st.error(
                    "Ocorreu um erro ao se comunicar "
                    f"com a API da Groq: {e}"
                )


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        PYCoder 🤖 - Assistente de programação Python
    </div>
    """,
    unsafe_allow_html=True
)
