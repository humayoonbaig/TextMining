# Deployment Guide - Legal RAG System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Vector Database Setup](#vector-database-setup)
4. [Running the System](#running-the-system)
5. [API Deployment](#api-deployment)
6. [Testing](#testing)
7. [Exam Submission](#exam-submission)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: 5GB for models and vector stores
- **OS**: Windows, macOS, or Linux

### API Keys Required
- **OpenAI API Key**: Required for GPT-4o-mini
  - Get it from: https://platform.openai.com/api-keys
  - Set in `.env` file

---

## Environment Setup

### Step 1: Clone/Extract the Repository

```bash
cd c:\Users\Dell\Desktop\humayun\TextMiningProject
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: Installation may take 5-10 minutes due to large packages (torch, transformers).

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your-openai-api-key-here
```

**To get your OpenAI API key**:
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`

---

## Vector Database Setup

### Step 1: Verify Data Structure

Ensure your `Contest_Data` folder has this structure:

```
Contest_Data/
├── Italy/
│   ├── Inheritance_italy/
│   ├── Divorce_italy/
│   └── Italian_cases_json_processed/
├── Estonia/
│   ├── Inheritance_estonia/
│   ├── Divorce_estonia/
│   └── Estonian_cases_json_processed/
└── slovenia/
    ├── Inheritance_slovenia/
    ├── Divorce_slovenia/
    └── Slovenian_cases_json_processed/
```

### Step 2: Build Vector Databases

**Option A: Using Streamlit UI (Recommended)**

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Navigate to **Settings** page:
   - Set LLM: `openai` / `gpt-4o-mini`
   - Set Embeddings: `huggingface` / `sentence-transformers/all-MiniLM-L6-v2`
   - Add data folders:
     - `Contest_Data/Italy`
     - `Contest_Data/Estonia`
     - `Contest_Data/slovenia`
   - Save configuration

3. Navigate to **Vector DB Builder** page:
   - Select all data folders
   - Set vector store name: `legal_all` (or separate by country)
   - Click "🔍 Scan folders & Build Vector DB"
   - Wait for completion (5-15 minutes)

**Option B: Using Python Script**

Create and run a build script:

```python
# build_vectordb.py
from backend.config import RAGConfig
from backend.document_loader import load_documents_from_folders
from backend.embeddings import get_embedding_model
from backend.vector_store import build_vector_store
import os

config = RAGConfig()
config.json_folders = [
    "Contest_Data/Italy",
    "Contest_Data/Estonia",
    "Contest_Data/slovenia"
]

# Load documents
print("Loading documents...")
docs = load_documents_from_folders(config.json_folders)
print(f"Loaded {len(docs)} documents")

# Build vector store
embedding_model = get_embedding_model(config)
vector_store_path = "vector_store/legal_all"
os.makedirs(vector_store_path, exist_ok=True)

print("Building vector database...")
build_vector_store(docs, embedding_model, vector_store_path)
print(f"Vector store created at: {vector_store_path}")
```

Run it:
```bash
python build_vectordb.py
```

### Step 3: Verify Vector Database

Check that `vector_store/` directory exists:

```
vector_store/
└── legal_all/
    ├── index.faiss
    └── index.pkl
```

---

## Running the System

### Streamlit Web Interface

**Start the app:**
```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

**Available pages:**
1. **Home**: Overview
2. **Settings**: Configure LLM, embeddings, and data paths
3. **Vector DB Builder**: Build/rebuild vector databases
4. **Chatbot Q&A**: Interactive chat interface
5. **RAG Evaluation**: RAGAS metrics dashboard

**Using the Chatbot:**
1. Go to "Chatbot Q&A" page
2. Select system mode in Settings (single-agent or multi-agent)
3. Ask questions like:
   - "What are the inheritance rules in Italy?"
   - "How do I file for divorce in Estonia?"
4. View sources and metadata
5. Save conversations for evaluation

### FastAPI Server (For Exam Submission)

**Start the API server:**

```bash
# Multi-agent mode (Task B) - DEFAULT
python run_api.py

# Single-agent mode (Task A)
python run_api.py --single-agent

# Custom port
python run_api.py --port 8080

# Development mode with auto-reload
python run_api.py --reload
```

**Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Test the API:**
```bash
curl http://localhost:8000/health
```

---

## API Deployment

### Running on a Server

**For Production Deployment:**

1. **Install dependencies on server:**
```bash
pip install -r requirements.txt
```

2. **Build vector databases** (one-time setup)

3. **Run with production settings:**
```bash
python run_api.py --host 0.0.0.0 --port 8000
```

4. **Use a process manager** (recommended):

**With systemd:**
```ini
# /etc/systemd/system/legal-rag.service
[Unit]
Description=Legal RAG API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/TextMiningProject
Environment="PATH=/path/to/env/bin"
Environment="OPENAI_API_KEY=your-key"
ExecStart=/path/to/env/bin/python run_api.py --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable legal-rag
sudo systemctl start legal-rag
sudo systemctl status legal-rag
```

### Docker Deployment (Optional)

The project includes a `Dockerfile`:

**Build image:**
```bash
docker build -t legal-rag-api .
```

**Run container:**
```bash
docker run -d \
  --name legal-rag \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  -v $(pwd)/vector_store:/app/vector_store \
  legal-rag-api
```

---

## Testing

### Step 1: Test the Internal Test Set

**Run the test suite:**
```bash
python test_api.py --url http://localhost:8000
```

This will:
- Test health check
- Test system info
- Run 5 sample questions from test set
- Compare single-agent vs multi-agent
- Save results to `test_results_<timestamp>.json`

### Step 2: Manual Testing

**Test single query:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the reserved portion for children in Italy?",
    "system": "multi-agent"
  }'
```

**Test batch query:**
```bash
curl -X POST http://localhost:8000/batch_query \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      "What are divorce grounds in Estonia?",
      "How is inheritance divided in Slovenia?"
    ],
    "system": "multi-agent"
  }'
```

### Step 3: Run RAGAS Evaluation

1. Use Streamlit app to create conversations
2. Save multiple chat sessions
3. Go to "RAG Evaluation" page
4. Edit ground truth labels
5. Click "Run RAGAS evaluation"
6. Review metrics

---

## Exam Submission

### Preparation Checklist

- [ ] Vector databases are built and tested
- [ ] API server runs without errors
- [ ] Test queries return valid responses
- [ ] OPENAI_API_KEY is valid and has credits
- [ ] Server has public IP or accessible URL
- [ ] Port 8000 (or your port) is open in firewall

### Submission Steps

1. **Ensure API is running:**
```bash
python run_api.py --host 0.0.0.0 --port 8000
# Leave this running!
```

2. **Verify endpoint is accessible:**
```bash
curl http://YOUR_PUBLIC_IP:8000/health
```

3. **Get your endpoint URL:**
- Format: `http://YOUR_IP:8000/query`
- Or use a domain: `https://your-domain.com/query`

4. **Submit to exam system:**
- Provide group member names
- Enter system descriptions:
  - **Single-agent**: "ReAct-style unified agent with semantic routing and country gate validation"
  - **Multi-agent**: "Supervisor agent coordinating specialized sub-agents per vector database"
- Enter endpoint URL: `http://YOUR_IP:8000/query`

5. **Monitor logs:**
```bash
# Watch for incoming requests
tail -f /var/log/legal-rag.log  # if using systemd
# or watch console output
```

### Important Notes

- ⚠️ **One-shot submission**: You cannot retry, so test thoroughly first
- ⚠️ **Keep server running**: Don't shut down during evaluation
- ⚠️ **Have API credits**: Ensure OpenAI account has sufficient credits
- ⚠️ **Response time**: System will receive 10 queries, must respond within timeout

---

## Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"

**Solution:**
```bash
# Ensure .env file exists
echo "OPENAI_API_KEY=sk-your-key" > .env

# Or set environment variable
export OPENAI_API_KEY=sk-your-key  # Linux/Mac
set OPENAI_API_KEY=sk-your-key     # Windows CMD
```

#### 2. "No module named 'backend'"

**Solution:**
```bash
# Ensure you're in project root
cd c:\Users\Dell\Desktop\humayun\TextMiningProject

# Run from project root
python run_api.py
```

#### 3. "Vector store not found"

**Solution:**
- Rebuild vector databases using Streamlit UI or build script
- Check that `vector_store/` directory exists
- Verify paths in Settings page

#### 4. "Out of memory" during vector DB build

**Solution:**
- Process countries separately
- Reduce batch size in `document_loader.py`
- Use a machine with more RAM

#### 5. API returns 500 errors

**Solution:**
- Check logs for detailed error
- Verify all dependencies installed
- Test with simple query first
- Check OpenAI API quota

#### 6. Slow response times

**Possible causes:**
- First query loads models (30-60s)
- Too many documents retrieved (reduce `top_k`)
- Large context sent to LLM (reduce `max_chars`)

**Solutions:**
- Keep API server running to avoid cold starts
- Adjust `top_k` in config (try 3-5)
- Enable caching

#### 7. RAGAS evaluation fails

**Common causes:**
- Missing ground truth in test set
- Empty contexts in chat history
- OpenAI API issues

**Solutions:**
- Ensure conversations include retrieved sources
- Edit ground truth in evaluation UI
- Check OpenAI API status

---

## Performance Optimization

### Speed Improvements

1. **Cache embedding model:**
   - Already implemented in `cached_get_embedding_model()`

2. **Reduce context size:**
   - Lower `top_k` in config (default: 5)
   - Reduce `max_chars` in context builder (default: 4000)

3. **Use smaller LLM for simple queries:**
   - Switch to `gpt-4o-mini` (already default)

4. **Pre-warm the API:**
   - Send a dummy query on startup to load models

### Cost Reduction

1. **Use fewer LLM calls:**
   - Single-agent mode uses ~2 calls per query
   - Multi-agent mode uses ~4+ calls per query

2. **Optimize prompts:**
   - Keep system prompts concise
   - Send only relevant context

3. **Batch queries:**
   - Use `/batch_query` endpoint for multiple questions

---

## Monitoring & Logging

### Enable Logging

Add to `backend/api_endpoint.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

### Monitor API Usage

Track in logs:
- Request timestamps
- Response times
- Error rates
- LLM API calls

---

## Security Considerations

1. **API Key Protection:**
   - Never commit `.env` to git
   - Use environment variables in production
   - Rotate keys periodically

2. **Rate Limiting:**
   - Consider adding rate limiting to API
   - Prevent abuse

3. **Input Validation:**
   - Already implemented via Pydantic models
   - Validates question format

4. **CORS:**
   - Currently allows all origins
   - Restrict in production: `allow_origins=["https://exam-system.com"]`

---

## Support & Contact

For issues or questions:
- Check `README.md` for overview
- See `ARCHITECTURE.md` for technical details
- Review code comments
- Contact: [Your Team Contact]

---

## Exam Submission Quick Start

**5-Minute Setup:**

```bash
# 1. Install and activate environment
python -m venv env
env\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Set API key
echo "OPENAI_API_KEY=your-key" > .env

# 3. Verify vector DBs exist (or build them)
ls vector_store/

# 4. Start API server
python run_api.py

# 5. Test endpoint
curl http://localhost:8000/health

# 6. Submit URL to exam system
# URL: http://YOUR_IP:8000/query
```

**You're ready!** 🚀
