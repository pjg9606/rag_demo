import os
import json
import streamlit as st

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from config.setting import OPENAI_API_KEY


def load_chunks(json_path="./parsed_data/law_chunks.json"):
    """
    law_chunks.json 로드
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def build_vectorstore(chunks):
    """
    law_chunks.json 데이터를 LangChain Document로 변환한 뒤
    HuggingFaceEmbeddings + FAISS VectorStore를 생성
    """
    docs = []
    for c in chunks:
        text = c["chunk_text"]
        meta = {
            "source": c["source"],
            "chunk_id": c["chunk_id"]
        }
        docs.append(Document(page_content=text, metadata=meta))

    # 임베딩 설정
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # FAISS VectorStore 생성
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def create_qa_chain(vectorstore):
    """
    RetrievalQA 체인 생성
     - LLM: ChatOpenAI (구버전 openai와 호환)
     - retriever: vectorstore.as_retriever(...)
    """

    # 1) OpenAI API 키 설정
    openai_api_key = OPENAI_API_KEY
    if not openai_api_key:
        st.warning("OPENAI_API_KEY가 설정되지 않았습니다.")

    # 2) ChatOpenAI 초기화
    #    "model_name" 대신 "model" 사용
    #    openai 0.28.0과 호환시키기 위함
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        temperature=0.0
    )

    # 3) Retriever 설정
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # 4) RetrievalQA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "map_reduce", "refine" 등도 가능
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain


def main():
    st.title("LangChain RAG Demo")
    st.write("법률 문서 RAG: LangChain + OpenAI + Streamlit 데모 버전")

    # 1) law_chunks.json 로드
    chunks = load_chunks()

    # 2) VectorStore 구축
    vectorstore = build_vectorstore(chunks)

    # 3) RetrievalQA 체인
    qa_chain = create_qa_chain(vectorstore)

    # 4) 사용자 질문 입력
    user_query = st.text_input("질문을 입력하세요:")
    if st.button("질문하기"):
        if user_query.strip():
            with st.spinner("답변 생성중..."):
                # RetrievalQA 체인을 호출
                result = qa_chain({"query": user_query})

                # 결과 파싱
                answer = result["result"]
                source_docs = result["source_documents"]

            # 출력
            st.subheader("답변")
            st.write(answer)

            st.subheader("참조 문서")
            for i, doc in enumerate(source_docs, start=1):
                source = doc.metadata.get("source", "N/A")
                chunk_id = doc.metadata.get("chunk_id", "N/A")
                st.write(f"**DOC {i}** - source: {source}, chunk_id: {chunk_id}")

                with st.expander("내용 보기"):
                    st.write(doc.page_content)
        else:
            st.warning("질문을 입력해주세요.")


if __name__ == "__main__":
    main()
