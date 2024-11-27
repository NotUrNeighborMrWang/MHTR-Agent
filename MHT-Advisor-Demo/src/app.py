import os
from datetime import datetime
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.chat_engine.types import ChatMode
from llama_index.llms.openai import OpenAI


log_dir = "./log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


log_file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")


def log_message(role, content):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {role}: {content}\n")

if __name__ == '__main__':
    @st.cache_resource(show_spinner=False)
    def load_data(model, temperature):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        Settings.llm = OpenAI(
            model=model,
            temperature=temperature,
            system_prompt="""
    Queries Regarding the Carburizing Heat Treatment Process:

    What is the basic principle of carburizing heat treatment?
    What types of furnaces are typically used for carburizing?
    How is carburizing depth measured?
    What are the typical temperatures and durations for carburizing treatment?
    What post-treatment procedures are required for materials after carburizing?
    How can uniformity and repeatability be ensured during the carburizing process?
    What specific effects does carburizing have on the mechanical properties of materials?
    Please discuss the advantages and disadvantages of carburizing compared to other surface hardening techniques, such as nitriding and carbo-nitriding.
    Please provide detailed explanations along with possible real-world application examples.
    """
        )
        index = VectorStoreIndex.from_documents(docs)
        return index


    st.title('🤖 Carburizing Heat Treatment Large Model App')
    st.caption('========== 💾 All responses are generated based on the local knowledge base and may not reflect real-time updates. Additionally, you need to load the local knowledge base into the ./data directory before starting. 💾 ==========')
    model_select = ('gpt-4o', 'gpt-4', 'gpt-3.5-turbo')

    with st.sidebar:
        option = st.selectbox(
            '🤖 Please select the large model engine 🤖',
            model_select
        )
        temperature = st.select_slider(
            "✨ Select the large model engine. Select the creativity index. ✨",
            [round(i * 0.1, 1) for i in range(1, 11)]
        )

    index = load_data(option, temperature)
    st.session_state["openai_model"] = option
    print('model: ' + st.session_state["openai_model"])

    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode=ChatMode.CONDENSE_QUESTION, verbose=True, streaming=True
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me a question!"):
        print('prompt: ' + prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        log_message("user", prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_stream = st.session_state.chat_engine.stream_chat(prompt)
                res = st.write_stream(response_stream.response_gen)
                print('response: ' + res)

        log_message("assistant", res)
        st.session_state.messages.append({"role": "assistant", "content": res})
