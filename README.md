# RAG Demo: 법률 문서 기반 LLM QA
- 이 저장소는 법률 문서(PDF)를 분할(Chunking) & 벡터 임베딩 후, LLM(GPT)과 결합한 RAG(Retrieval-Augmented Generation) 기반 질의응답 챗봇 입니다.
- LangChain Community + HuggingFaceEmbeddings + FAISS + OpenAI GPT로 구성했으며, Streamlit UI를 통해 웹 상에서 질문을 입력하고 답변을 받을 수 있습니다.
- 데이터는 국가법령정보센터(https://www.law.go.kr/) 의 자료를 이용하였습니다.
## 프로젝트 개요
- LangChain과 OpenAI API를 활용한 법률 문서 기반 RAG 시스템
- 사용자가 입력한 질문에 대해 법률 문서에서 정보를 검색하고, AI가 답변을 생성
- 법률 문서를 효과적으로 파싱하고 검색 가능한 형식으로 변환
- 데이터셋: 법률 문서 PDF(예: 형법, 근로기준법 등)를 ./data/ 폴더에 저장
- 전처리: parse_pdfs.py 실행 시, PDF에서 텍스트 추출 후 chunk 단위로 분할 → law_chunks.json 생성
- 벡터 인덱스: app.py 내에서 HuggingFaceEmbeddings로 임베딩 & FAISS VectorStore 빌드
- LLM 질의응답: OpenAI GPT (gpt-3.5-turbo 등)를 호출해, 검색된 문서 조각(Top-k)을 참고하여 답변 생성
- UI: Streamlit 기반 웹 인터페이스

## 주의:
- 오로지 데모 목적으로 제작되었으며, 실제 법률 자문 수준의 정확도를 보장하진 않습니다.
- openAI API Key가 필요하므로, .env 파일 등을 통해 비공개로 관리해 주세요.

## 기술 스택
- **LLM**: OpenAI GPT (gpt-3.5-turbo)
- **프레임워크**: LangChain
- **데이터 저장소**: FAISS(Vector DB)
- **웹 프레임워크**: Streamlit
- **문서 처리**: pdfplumber

## 프로젝트 구조
```
rag_demo/
├─ data/
│   ├─ (법률 PDF 파일들)
├─ parsed_data/
│   └─ law_chunks.json    #parse_pdfs.py 실행결과
├─ parse_pdfs.py      
├─ app.py              
├─ .env                
├─ requirements.txt    
├─ .gitignore          
└─ README.md           

```

## 설치 및 실행 방법
### 1. 환경 설정
필요한 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. PDF 전처리
data 폴더의 PDF 문서들을 스캔해 텍스트 추출 & 전처리
/parsed_data/law_chunks.json 파일 생성
```bash
python parse_pdfs.py
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고, OpenAI API 키를 추가합니다.
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. 애플리케이션 실행
```bash
streamlit run app.py
```

## 참고
- OpenAI API Key를 .env 또는 환경변수로 설정해야 합니다.
- .env 파일에 OPENAI_API_KEY=sk-xxxxx 작성 후 .gitignore에 .env 추가.

