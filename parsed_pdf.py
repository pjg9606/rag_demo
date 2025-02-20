import os
import re
import json
import pdfplumber

# ------------------------------------------------
# 1) PDF -> 텍스트 추출 함수
# ------------------------------------------------
def pdf_to_text(pdf_path):
    """
    pdf_path: PDF 파일 경로
    return: 해당 PDF에서 추출한 전체 텍스트 (string)
    """
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 각 페이지마다 텍스트 추출
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text


# ------------------------------------------------
# 2) 텍스트 전처리 & Cleaning
# ------------------------------------------------
def clean_text(text):
    """
    text: PDF에서 추출된 원본 텍스트
    return: 기본적인 정규식/공백 제거 등 간단한 전처리를 마친 텍스트
    """
     # 1) 여러 줄바꿈 -> 단일 줄바꿈
    text = re.sub(r'\n+', '\n', text)
    # 2) 2개 이상 공백 -> 1개
    text = re.sub(r'[ ]+', ' ', text)
    # 3) 특수문자(예시) 제거
    text = re.sub(r'[■□◆◇▲△▶]', '', text)
    # 4) 앞뒤 공백 제거
    text = text.strip()

    return text


# ------------------------------------------------
# 3) 텍스트 Chunking
# ------------------------------------------------
def chunk_text_by_tokens(text, chunk_size=300, overlap=50):
    """
    text: 전처리된 텍스트 (하나의 긴 문자열)
    return: chunk(문자열)들의 리스트
    """
    tokens = text.split()
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        # chunk를 다시 문자열로
        chunk_str = " ".join(chunk).strip()
        chunks.append(chunk_str)

        # overlap을 적용하여 다음 chunk 시작점 계산
        start = end - overlap
        if start < 0:
            start = 0

        # 혹시 start가 리스트 끝을 넘어서면 break
        if start >= len(tokens):
            break

    return chunks


# ------------------------------------------------
# 4) PDF -> Text -> Clean -> Chunk + 저장
# ------------------------------------------------
def process_pdf(pdf_path, chunk_size=300, overlap=50):
    """
    pdf_path: PDF 경로
    return: chunk 관련 정보
    """
    # (1) PDF에서 텍스트 추출 및 텍스트 전처리
    raw_text = pdf_to_text(pdf_path)
    cleaned = clean_text(raw_text)

    # (2) chunk 나누기
    chunk_list = chunk_text_by_tokens(cleaned, chunk_size, overlap)

    # (3) 각 chunk에 메타데이터(출처, chunk ID 등) 부여
    result = []
    for i, chunk in enumerate(chunk_list):
        # 파일명이나 다른 식별자 + chunk index
        result.append({
            "chunk_text": chunk,
            "source": os.path.basename(pdf_path),
            "chunk_id": i
        })

    return result


def main():
    pdf_dir = "./data"
    output_dir = "./parsed_data"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_chunks = []

    # data 폴더 내부의 모든 PDF 반복
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"Processing PDF: {pdf_path}")

            # PDF -> chunk 리스트
            chunks = process_pdf(
                pdf_path,
                chunk_size=300, 
                overlap=50       
            )

            all_chunks.extend(chunks)

    # 최종적으로 하나의 JSON 파일에 저장
    output_path = os.path.join(output_dir, "law_chunks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"=== Job Done, Total Chunks: {len(all_chunks)} ===")
    print(f"=== Saved at: {output_path} ===")


if __name__ == "__main__":
    main()
