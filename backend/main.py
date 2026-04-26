from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_url

from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Query(BaseModel):
    url: str
    question: str

# embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

@app.post("/ask")
def ask_question(query: Query):
    try:
        print("\n🔥 ===== NEW REQUEST =====")
        print("🔗 URL:", query.url)
        print("❓ Question:", query.question)

        # 1. SCRAPE
        text = scrape_url(query.url)

        if not text:
            return {"answer": "No content extracted from URL"}

        print("📄 Length:", len(text))

        # 2. CHUNKING
        splitter = CharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=1000
        )
        docs = splitter.create_documents([text])

        print("📦 Docs:", len(docs))

        # 3. VECTOR DB
        db = Chroma.from_documents(docs, embeddings)

        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "fetch_k": 10,
                "lambda_mult": 0.7
            }
        )

        # 4. RETRIEVE
        relevant_docs = retriever.invoke(query.question)

        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        if not context.strip():
            context = text[:1500]

        print("🔍 Context length:", len(context))

        # 5. PROMPT
        prompt = f"""
You are a strict assistant.

Rules:
- Use ONLY context
- If answer not in context, say "I don't know"
- Do not hallucinate
- Be detailed
Context:
{context}

Question:
{query.question}

Answer:
"""

        # 🔥 GEMINI CALL
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )

        answer = response.text

        print("🧠 Answer:", answer)

        db.delete_collection()
        
        return {"answer": answer}
        

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"answer": str(e)}