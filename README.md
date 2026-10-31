# Summative Lab: Local RAG-Powered Knowledge Assistant

## Overview

In this summative lab, you will complete a local full-stack AI application that helps users ask questions about a small approved knowledge base.

The starter app includes a React frontend, a Flask backend, starter API routes, knowledge base files, environment configuration, and TODO comments in the key backend files. Your job is to complete the backend AI workflow so the frontend can send a question, the backend can retrieve relevant context, and the app can return a source-backed answer.

You will not deploy this application. You will run it locally and focus on connecting the frontend, backend, vector database, model service, and RAG workflow.

## Scenario

Your team is building a local prototype of an internal knowledge assistant. Employees need quick answers from a small set of approved documents, such as onboarding notes, product support guidance, security expectations, and workplace FAQs.

The frontend team has already created a simple chat interface. A user can type a question and submit it. However, the backend AI workflow is incomplete. The app still needs to retrieve relevant knowledge base content, send that context to the model, and return an answer with supporting sources.

Your role is to complete the backend AI functionality so the team can review whether the prototype is useful before deciding what to improve next.

## Learning Goal

You will complete a local full-stack AI application by connecting a React frontend, Flask backend, vector database, knowledge base, and model service into a working RAG workflow that returns useful answers with supporting sources.

By completing this lab, you will:

- Complete a Flask API route that receives user questions.
- Connect the backend to a local model service.
- Store and retrieve knowledge base chunks using a vector database.
- Build a RAG workflow that uses retrieved context to generate an answer.
- Return both an answer and supporting sources to the frontend.
- Use environment variables for key configuration values.
- Document how to install, run, and check the application.

## Scope

This lab focuses on building a local RAG-powered full-stack application.

You are not required to add:

- Authentication
- Pagination
- Deployment
- A new frontend from scratch
- A large custom knowledge base
- Automated test files

When this lab asks you to test or check your work, it means you should run the app locally, try sample questions, review the output, and refine the code based on what you observe.

## Tools and Resources

You will use:

- Python 3.10+
- Flask
- React + Vite
- Node.js and npm
- Chroma or the approved local vector store included in the starter
- Ollama or another approved local model service
- Git and GitHub
- A `.env` file for configuration

Recommended Ollama models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Project Structure

```text
summative-rag-knowledge-assistant-starter/
├── client/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── styles.css
├── server/
│   ├── app.py
│   ├── config.py
│   ├── documents.py
│   ├── rag_service.py
│   ├── seed_knowledge_base.py
│   ├── vector_store.py
│   ├── requirements.txt
│   ├── Pipfile
│   ├── .env.example
│   └── knowledge_base/
│       ├── onboarding.txt
│       ├── product_support.txt
│       ├── security_guidelines.txt
│       └── workplace_faq.txt
└── README.md
```

## What Is Already Provided

The starter repository includes:

- A React frontend interface
- A Flask backend structure
- A working `/api/health` route
- A starter `/api/ask` route
- Knowledge base documents in plain text format
- A document loading and chunking helper
- Starter files for vector retrieval and RAG workflow code
- Environment variable examples
- TODO comments showing where you need to complete the implementation

## What You Need to Complete

You are responsible for completing the main backend AI workflow.

You will complete TODOs in:

- `server/app.py`
- `server/vector_store.py`
- `server/rag_service.py`

Your completed app should allow a user to:

1. Open the React frontend.
2. Type a question about the knowledge base.
3. Submit the question to the Flask backend.
4. Retrieve relevant knowledge base chunks from the vector database.
5. Send the question and retrieved context to the model service.
6. Receive a generated answer.
7. View supporting sources in the frontend.

---

## Instructions

### Task 1: Define the Problem

Start by reviewing the starter app, scenario, and provided knowledge base documents.

Identify the problem your AI assistant is designed to solve:

- Who will use this assistant?
- What kind of questions should the assistant help answer?
- What approved knowledge base content will the assistant use?
- What should a useful answer include?
- Why is a source-backed answer important for this use case?

In this README, replace the placeholder section below with a short description of the user need and the purpose of your assistant.

#### Response: Problem Definition

New employees and support agents often waste time hunting through onboarding notes, support guides and policies to find one answer. This assistant lets them type a plain-English question and get a short answer based only on the approved knowledge base. Every answer comes with the source documents it used, so people can check the original text instead of trusting a confident-sounding reply. If the knowledge base does not contain the answer, the assistant says so instead of guessing.

---

### Task 2: Determine the Design

Plan how the provided frontend, Flask backend, vector database, RAG workflow, and model service will work together.

Review the starter code and identify:

- Where the frontend sends user questions
- Which backend route receives the question
- Where the RAG workflow should be completed
- Where the knowledge base files are stored
- How source information should be returned
- Which environment variables are needed

Your design should account for:

- The backend question route
- Knowledge base loading and chunking
- Vector database setup
- Retrieval of relevant chunks
- Prompt construction
- Model service connection
- JSON response format for the frontend
- Display of answers and sources in the frontend

You do not need to build a new frontend from scratch. Use the provided frontend and make only the adjustments needed to connect it to your completed backend workflow.

#### Response: Design Notes

```text
User browser
→ React frontend (client/src/App.jsx, POST /api/ask)
→ Flask /api/ask route (server/app.py): validates the question
→ RAG workflow (server/rag_service.py)
→ Vector database retrieval (server/vector_store.py + Chroma)
   - question is embedded with Ollama (nomic-embed-text)
   - the closest chunks are returned with source metadata
→ Prompt is built from the question + retrieved chunks
→ Model service (Ollama llama3.2, /api/generate)
→ { answer, sources } returned to the frontend and displayed
```

- Knowledge base files live in `server/knowledge_base/` and are split into overlapping 120-word chunks by `documents.py`.
- Each chunk is stored in Chroma with `source`, `title` and `chunk_index` metadata so the frontend can show sources.
- Settings (models, paths, TOP_K, temperature) come from `server/.env`.

---

### Task 3: Develop, Test, and Refine the Code

Complete the required code so the local full-stack AI assistant works from the frontend through the backend RAG workflow.

Your implementation should:

- Configure your local `.env` file using `.env.example`.
- Complete the backend route that receives a user question.
- Load the provided knowledge base documents.
- Create or update retrievable chunks in the vector database.
- Preserve source information for returned chunks.
- Retrieve relevant context based on the user’s question.
- Build a prompt using the retrieved context.
- Send the prompt to the model service.
- Return a JSON response with:
  - The generated answer
  - Supporting sources
  - Any relevant metadata included in the starter structure
- Connect the backend response to the frontend display.

After developing the core workflow, run the application locally and try at least three sample questions.

For each sample question, check:

- Does the frontend submit the question successfully?
- Does the backend return a response?
- Is the answer relevant to the question?
- Does the response include useful supporting sources?
- Are there errors in the terminal or browser console?
- Does anything need to be refined for clarity, relevance, or reliability?

Refine your code based on what you find.

#### Response: Sample Questions and Observations

See the Sample Questions section below for the results table.

---

### Task 4: Document and Maintain

Prepare your project for review and submission.

Your GitHub repository should include:

- Completed backend question route
- Completed RAG workflow
- Vector database setup or setup instructions
- Provided knowledge base documents
- Working frontend/backend connection
- `.env.example`
- Dependency files
- README
- Meaningful Git commit history

Your README should include:

- Project title
- Project description
- User need or scenario
- Installation instructions
- Run instructions
- Required environment variables
- API route descriptions
- Description of the RAG workflow
- At least three sample questions you tried
- Notes about whether the answers and sources were relevant
- Known limitations or future improvements

Before submitting:

1. Save your work with Git.
2. Commit your changes with meaningful commit messages.
3. Push your final work to GitHub.
4. Submit your GitHub repository link in Canvas.

---

## Setup Instructions

### 1. Start Ollama

In a terminal, confirm Ollama is running and pull the recommended models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama run llama3.2 "Reply with one short sentence."
```

### 2. Set Up the Flask Backend

From the project root:

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

After activating, confirm you are really using the project's virtual environment:

```bash
which python    # should end with server/.venv/bin/python
hash -r
```

If you see `ModuleNotFoundError` (for example `No module named 'flask'`) or `Error: No such command 'run'`, the virtual environment is not active. Run `source .venv/bin/activate` again in that terminal and re-run `pip install -r requirements.txt`.

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Complete the Backend TODOs

Open these files and complete the TODO comments:

- `server/app.py`
- `server/vector_store.py`
- `server/rag_service.py`

The app will not fully work until these TODOs are completed.

### 4. Seed the Knowledge Base

After completing the vector store TODOs, run:

```bash
python seed_knowledge_base.py
```

This script loads the provided knowledge base files, chunks the text, creates embeddings, and stores the chunks in the vector database.

### 5. Run the Flask Backend

```bash
flask --app app run --debug --port 5555
```

You should be able to visit:

```text
http://localhost:5555/api/health
```

Expected response:

```json
{
  "message": "Backend is running.",
  "status": "ok"
}
```

### 6. Set Up and Run the React Frontend

Open a second terminal from the project root:

```bash
cd client
npm install
npm run dev
```

Open the local frontend URL shown in your terminal. It is usually:

```text
http://localhost:5173
```

---

## API Routes

### GET `/api/health`

Confirms that the backend is running.

Expected response:

```json
{
  "status": "ok",
  "message": "Backend is running."
}
```

### POST `/api/ask`

Receives a user question and returns an answer with sources.

Expected request body:

```json
{
  "question": "What should I do if I cannot log into the product dashboard?"
}
```

Expected response format:

```json
{
  "answer": "A helpful answer grounded in the knowledge base.",
  "sources": [
    {
      "title": "Product Support Guide",
      "source": "product_support.txt",
      "chunk_index": 0,
      "excerpt": "Relevant source excerpt..."
    }
  ]
}
```

---

## Environment Variables

Create your local `.env` file from `server/.env.example`.

| Variable | Purpose |
|---|---|
| `OLLAMA_BASE_URL` | URL for the local model service |
| `GENERATION_MODEL` | Model used to generate answers |
| `EMBEDDING_MODEL` | Model used to create embeddings |
| `CHROMA_PATH` | Local folder where Chroma stores vector data |
| `COLLECTION_NAME` | Name of the vector collection |
| `KNOWLEDGE_BASE_PATH` | Folder containing source documents |
| `TOP_K` | Number of chunks to retrieve |
| `TEMPERATURE` | Controls response variation |
| `CLIENT_ORIGIN` | Local frontend origin allowed by the backend |

Example values:

```text
OLLAMA_BASE_URL=http://localhost:11434
GENERATION_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text
CHROMA_PATH=./chroma_db
COLLECTION_NAME=knowledge_assistant
KNOWLEDGE_BASE_PATH=./knowledge_base
TOP_K=3
TEMPERATURE=0.2
CLIENT_ORIGIN=http://localhost:5173
```

---

## Knowledge Base Files

The starter app includes these source files:

- `server/knowledge_base/onboarding.txt`
- `server/knowledge_base/product_support.txt`
- `server/knowledge_base/security_guidelines.txt`
- `server/knowledge_base/workplace_faq.txt`

These files are the approved source content for the assistant. The RAG workflow should retrieve from these files and return sources that help users understand where the answer came from.

You may make small edits to the source files if allowed or instructed to by your instructor.

---

## RAG Workflow Description

1. The React frontend sends `{ "question": "..." }` to `POST /api/ask`.
2. `app.py` checks that the question is a non-blank string (otherwise it returns a 400 error) and passes it to `answer_question()` in `rag_service.py`.
3. `retrieve_relevant_chunks()` in `vector_store.py` asks Ollama to turn the question into an embedding, then queries Chroma for the `TOP_K` closest chunks (cosine distance).
4. If nothing is found, the assistant returns a safe "not enough information" message and an empty `sources` list, and the model is never called.
5. Otherwise `build_prompt()` combines the question with the retrieved chunks and tells the model to use only that context.
6. `call_generation_model()` sends the prompt to Ollama's `/api/generate` endpoint (non-streaming, temperature from `.env`).
7. The route returns `{ "answer": "...", "sources": [ { title, source, chunk_index, excerpt } ] }` and the frontend displays both.
8. If Ollama is not running or a model is missing, the route returns a 502 with a helpful message that the frontend shows in its error box.

---

## Sample Questions

Try at least three sample questions after your implementation is complete.

You may use these sample questions or write your own:

1. What should I do if I cannot log into the product dashboard?
2. Why are source-backed answers important?
3. What should employees do if they receive a suspicious email?
4. What should a support agent do if the knowledge base does not answer a customer question?
5. What should a new employee complete during the first week?

Record your observations in the table below.

| Sample Question | Was the Answer Relevant? | Were Useful Sources Returned? | Notes |
|---|---|---|---|
|What should I do if I cannot log into the product dashboard?  | yes |yes  |Source: Product Support Guide | product_support.txt| 
|What should employees do with suspicious emails?  |yes |yes  |Source: Security Guidelines | security_guidelines.txt  |
|What should a support agent do if the knowledge base does not answer a question?  |yes  |yes  |Source 1: Workplace FAQ and Source 2: Product Support Guide|

---

## Known Limitations or Future Improvements

- The knowledge base is only four short files, so some questions cannot be answered.
- Chunks are split by word count, not by section, so a chunk can start in the middle of a sentence.
- There is no similarity cutoff: the closest chunks are always returned, even for an unrelated question. The prompt tells the model to say when the context is not enough, but a distance threshold would be more reliable.
- Re-run `python seed_knowledge_base.py` after editing a knowledge base file. If you delete or rename a file, delete the `chroma_db` folder first so old chunks do not stay behind.
- Answers depend on the small local model (llama3.2) and can still be imperfect, so important answers should be checked against the sources.
- No chat history, streaming responses or user feedback buttons yet.

---

## Submission Checklist

Before submitting, confirm that:

- The backend starts successfully.
- The frontend loads successfully.
- The frontend can submit a question to the backend.
- The backend retrieves relevant context from the vector database.
- The model service returns an answer.
- The answer is displayed in the frontend.
- Supporting sources are displayed in the frontend.
- Your `.env.example` is included.
- Your actual `.env` file is not committed.
- Your README is updated with required sections.
- Your Git commits have meaningful messages.
- Your final work is pushed to GitHub.

Submit your public GitHub repository link in Canvas.