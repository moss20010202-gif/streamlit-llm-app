from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- LLM処理関数 ---
def get_llm_response(user_input, persona_type):
    """
    入力テキストとラジオボタンの選択値を受け取り、LLMの回答を返す
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # 選択された専門家に応じてシステムメッセージを定義
    if persona_type == "IT技術コンサルタント":
        system_message = "あなたは熟練のIT技術コンサルタントです。技術的な課題に対して、論理的で実装可能なアドバイスを提供してください。"
    else:
        system_message = "あなたは世界的に有名な料理研究家です。初心者でも美味しく作れるコツや、食材の活かし方を情熱的に解説してください。"

    # プロンプトテンプレートの設定
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}")
    ])

    # チェインの作成
    chain = prompt | llm | StrOutputParser()
    
    # 実行
    return chain.invoke({"input": user_input})

# --- UI部分 (Streamlit) ---
st.set_page_config(page_title="AI Expert Chat", layout="centered")

st.title("🤖 AI専門家相談室")
st.write("""
このアプリでは、選択した専門家から回答を得ることができます。
1. **相談したい内容**を入力フォームに記入してください。
2. **専門家の種類**をラジオボタンで選択してください。
3. 送信ボタンを押すと、AIが指定された専門家として回答します。
""")

with st.form("my_form"):
    # テキスト入力
    user_input = st.text_area("相談内容を入力してください:", placeholder="例：Pythonの学習方法を教えて / 今日の夕飯の献立を提案して")
    
    # ラジオボタン
    persona_type = st.radio(
        "相談する専門家を選択してください:",
        ("IT技術コンサルタント", "料理研究家")
    )
    
    # 送信ボタン
    submitted = st.form_submit_button("回答を生成する")

if submitted:
    if user_input:
        with st.spinner("思考中..."):
            try:
                response = get_llm_response(user_input, persona_type)
                st.subheader(f"✨ {persona_type}からの回答")
                st.write(response)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("相談内容を入力してください。")