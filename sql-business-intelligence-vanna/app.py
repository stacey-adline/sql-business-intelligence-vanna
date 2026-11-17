import streamlit as st
import pandas as pd
from src.database import run_read_query, get_connection
from src.vanna_client import create_vanna_client

st.set_page_config(page_title="Vanna Business Intelligence", page_icon="🤖", layout="wide")
st.title("🤖 SQL Business Intelligence with Vanna AI")
st.caption("Ask questions about the demo business database in natural language.")

SUGGESTIONS = [
    "What is the total sales amount?",
    "Show sales by region.",
    "Which five products have the highest sales?",
    "Show monthly sales for 2025.",
    "Which are the top five customers by sales?",
    "Which sub-category has the lowest total profit?",
]

with st.sidebar:
    st.header("Example questions")
    for q in SUGGESTIONS:
        st.markdown(f"- {q}")
    st.divider()
    st.caption("Demo data: 500 synthetic order lines for 2025.")

@st.cache_resource
def get_vn():
    return create_vanna_client()

try:
    vn = get_vn()
except Exception as exc:
    st.error(str(exc))
    st.info("Create a .env file from .env.example, add your OpenAI API key, then run `python -m src.seed_data` and `python -m src.train`.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sql"):
            st.code(message["sql"], language="sql")
        if message.get("data") is not None:
            st.dataframe(pd.DataFrame(message["data"]), use_container_width=True)

question = st.chat_input("Ask a business question, e.g. What are total sales by region?")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Generating SQL..."):
            try:
                sql = vn.generate_sql(question=question)
                if not sql:
                    raise ValueError("Vanna did not return a SQL query. Try rephrasing your question.")
                rows = run_read_query(sql)
                result = [dict(row) for row in rows]
                st.markdown("**Generated SQL**")
                st.code(sql, language="sql")
                st.markdown("**Query results**")
                st.dataframe(pd.DataFrame(result), use_container_width=True)
                answer = f"Query completed successfully. Returned {len(result)} row(s)."
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant", "content": answer, "sql": sql, "data": result
                })
            except Exception as exc:
                error = f"Could not complete the query: {exc}"
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})
