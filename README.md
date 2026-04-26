# WebPal – AI-powered RAG Chrome Extension

WebPal is a Chrome Extension that allows you to ask questions directly from any webpage using AI.

It scrapes the webpage, processes the content, and gives accurate answers using Retrieval-Augmented Generation (RAG).

---

##  Features

*  Ask questions from any webpage
*  Fast responses using embeddings + vector search
*  Uses Gemini for intelligent answers
*  Context-aware (answers only from webpage content)
*  Smart chunking + retrieval (MMR search)

---

## Tech Stack

### Backend

* FastAPI
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Google Gemini API

### Frontend(basic)
* JavaScript

---

## How it Works

1. User opens a webpage
2. Extension sends URL + question
3. Backend:

   * Scrapes webpage
   * Splits into chunks
   * Converts into embeddings
   * Stores in vector DB
4. Relevant chunks retrieved
5. Gemini generates final answer

---

##  Backend Setup

### 1. Clone repository

```bash
git clone https://github.com/rrawat10/WebPal.git
cd WebPal/backend
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run backend

```bash
uvicorn main:app --reload
```

---

##  How to Load Chrome Extension

1. Open Chrome and go to:

   ```
   chrome://extensions/
   ```

2. Enable **Developer Mode** 

3. Click **Load unpacked**

4. Select the `extension` folder from this project

5. Extension will appear in toolbar 🎉

---

## 🚀 How to Use WebPal

1. Open any webpage (blog/article recommended)
2. Click WebPal extension icon
3. Enter your question
4. Click **Ask**
5. Get AI answer based only on webpage

---

## ⚠️ Important Notes

* Backend must be running:

  ```
  uvicorn main:app --reload
  ```
* Do not close terminal while using extension
* Works best on text-heavy pages

---

## 🧪 API Endpoint

POST `/ask`

### Body:

```json
{
  "url": "https://example.com",
  "question": "What is this page about?"
}
```

---

