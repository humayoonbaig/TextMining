# Legal RAG System - Multi-National Civil Law Query System


This project implements a Retrieval-Augmented Generation (RAG) system for querying civil law across Italy, Estonia, and Slovenia, covering **Inheritance** and **Divorce** law.

**Goal**: Compare two architectural strategies (single-agent vs multi-agent) for intelligent routing across multinational legal datasets.

---

## 🎯 Core Deliverables

✅ **Two RAG System Implementations**
- **Task A**: Single-Agent ReAct system ([backend/rag_single_agent.py](backend/rag_single_agent.py))
- **Task B**: Multi-Agent Supervisor system ([backend/rag_multiagent.py](backend/rag_multiagent.py))

✅ **Interactive Chat Interface** with transparency features ([pages/3_Chatbot_QA.py](pages/3_Chatbot_QA.py))
- Natural language Q&A
- Source attribution with metadata
- JSON conversation logging

✅ **RAGAS Evaluation Dashboard** ([pages/4_RAG_Evaluation.py](pages/4_RAG_Evaluation.py))
- Context Precision & Recall
- Faithfulness & Answer Relevancy
- Answer Correctness vs ground truth

✅ **REST API Endpoint** for exam submission ([backend/api_endpoint.py](backend/api_endpoint.py))
- FastAPI with OpenAPI docs
- Supports both single and multi-agent modes
- Production-ready

✅ **Complete Documentation Package**
- [ARCHITECTURE.md](ARCHITECTURE.md) - Flowcharts, component details, model justifications
- [PRESENTATION.md](PRESENTATION.md) - 12-slide presentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Setup and deployment guide
- [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) - Exam submission checklist

---

## 🏗 Architecture Overview

### Task A: Single-Agent (ReAct)

A unified agent using **Reasoning + Acting** pattern:

```
User Question → Decide Retrieval Need → Semantic Selection →
Country Gate → Vector Search → Answer Generation
```

**Key Features:**
- Explicit reasoning about retrieval necessity
- Semantic routing (countries + content types)
- Article-aware prioritization
- Similarity re-ranking

### Task B: Multi-Agent (Supervisor)

Hierarchical system with **specialized sub-agents**:

```
User Question → Supervisor Routes to Agents →
Sub-Agents Retrieve Independently → Supervisor Synthesizes Answer
```

**Key Features:**
- Specialized agents per vector database
- Parallel retrieval
- Conflict resolution & synthesis
- Better scalability

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed flowcharts and comparison.

---

## 📂 Dataset Structure

```
Contest_Data/
├── Italy/
│   ├── Inheritance_italy/      (Civil code articles)
│   ├── Divorce_italy/
│   └── Italian_cases_json_processed/  (Court cases)
├── Estonia/
│   ├── Inheritance_estonia/
│   ├── Divorce_estonia/
│   └── Estonian_cases_json_processed/
└── slovenia/
    ├── Inheritance_slovenia/
    ├── Divorce_slovenia/
    └── Slovenian_cases_json_processed/
```

**Content Types:**
- Civil Code Articles (legal provisions)
- Court Case Rulings (with metadata: cost, duration, parties, etc.)

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 2. Build Vector Databases

**Option A: Streamlit UI (Recommended)**
```bash
streamlit run app.py
# Navigate to: Settings → Add data folders → Vector DB Builder
```

**Option B: Python Script**
```python
# See DEPLOYMENT.md for build script
```

### 3. Run the System

**Streamlit Web Interface:**
```bash
streamlit run app.py
# Access at: http://localhost:8501
```

**FastAPI Server (for exam):**
```bash
# Multi-agent mode (Task B)
python run_api.py

# Single-agent mode (Task A)
python run_api.py --single-agent

# API docs at: http://localhost:8000/docs
```

### 4. Test the System

```bash
# Run automated test suite
python test_api.py

# Test single query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is inheritance law in Italy?", "system": "multi-agent"}'
```

---

## 📊 Evaluation with RAGAS

**Internal Test Set:** 12 questions in [test_set.json](test_set.json)

**Metrics Computed:**
1. **Context Precision**: Relevance of retrieved docs (0-1)
2. **Context Recall**: Coverage of needed info (0-1)
3. **Faithfulness**: Grounding in sources (0-1)
4. **Answer Relevancy**: Addresses question (0-1)
5. **Answer Correctness**: Match with ground truth (0-1)

**Run Evaluation:**
1. Create conversations in Streamlit chatbot
2. Save chat sessions
3. Go to "RAG Evaluation" page
4. Add ground truth labels
5. Click "Run RAGAS evaluation"

---

## 🔧 Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Embedding Model** | sentence-transformers/all-MiniLM-L6-v2 | Open-source, fast, good quality |
| **Generative LLM** | GPT-4o-mini (OpenAI) | Cost-effective, excellent reasoning |
| **Vector Database** | FAISS | Fast similarity search, persistent |
| **Web Framework** | Streamlit | Interactive UI, rapid prototyping |
| **API Framework** | FastAPI | Production-ready, auto docs |
| **Orchestration** | LangChain | RAG pipeline abstraction |
| **Evaluation** | RAGAS | Standard RAG metrics |

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed model justifications.

---

## 📁 Project Structure

```
TextMiningProject/
├── app.py                      # Streamlit main app
├── run_api.py                  # FastAPI server launcher
├── test_api.py                 # API test script
├── test_set.json               # Internal test questions
├── backend/
│   ├── config.py               # Configuration management
│   ├── document_loader.py      # JSON document loader
│   ├── embeddings.py           # Embedding model
│   ├── llm_provider.py         # LLM wrapper
│   ├── vector_store.py         # FAISS vector DB
│   ├── rag_single_agent.py     # Task A implementation
│   ├── rag_multiagent.py       # Task B implementation
│   ├── rag_pipeline.py         # Unified pipeline
│   ├── api_endpoint.py         # FastAPI endpoints
│   └── ...
├── pages/
│   ├── 1_Settings.py           # Configuration UI
│   ├── 2_Vector_DB_Builder.py  # DB builder UI
│   ├── 3_Chatbot_QA.py         # Chat interface
│   └── 4_RAG_Evaluation.py     # RAGAS evaluation UI
├── Contest_Data/               # Legal documents dataset
├── vector_store/               # Built FAISS databases
├── ARCHITECTURE.md             # Architecture documentation
├── PRESENTATION.md             # Presentation slides
├── DEPLOYMENT.md               # Deployment guide
├── SUBMISSION_CHECKLIST.md     # Exam checklist
└── README.md                   # This file
```

---

## 🎓 Exam Submission

### API Endpoint Format

**URL:** `http://YOUR_IP:8000/query`

**Request:**
```json
{
  "question": "What are the inheritance rules in Italy?",
  "system": "multi-agent"  // or "single-agent"
}
```

**Response:**
```json
{
  "question": "...",
  "answer": "...",
  "contexts": ["...", "..."],
  "source_ids": ["...", "..."],
  "metadata": {
    "system": "multi-agent",
    "num_sources": 5,
    "countries_covered": ["ITALY"],
    "law_types_covered": ["Inheritance"]
  }
}
```

### Pre-Submission Checklist

See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for complete checklist.

**Critical items:**
- [ ] Vector databases built
- [ ] API server running and accessible
- [ ] OpenAI API key valid with credits
- [ ] Test suite passes
- [ ] Endpoint URL verified

**Submission Info:**
- **Single-Agent Description**: See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- **Multi-Agent Description**: See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- **Endpoint URL**: `http://YOUR_IP:8000/query`

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview (this file) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detailed architecture, flowcharts, model justifications |
| [PRESENTATION.md](PRESENTATION.md) | 12-slide presentation covering all aspects |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Setup, deployment, and troubleshooting guide |
| [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) | Exam submission preparation checklist |

---

## 🔍 Key Features

### Transparency & Explainability
- Full source attribution with metadata
- Reasoning trace logs (optional)
- JSON conversation logging
- Retrieval visualization

### Intelligent Routing
- Semantic selection of countries/content
- Country gate validation
- Article-aware prioritization
- Similarity-based re-ranking

### Scalability
- Multi-database support
- Specialized agent architecture
- Parallel retrieval (multi-agent)
- Easy to add new jurisdictions

### Production Ready
- FastAPI with OpenAPI docs
- Error handling
- Input validation (Pydantic)
- Health checks & monitoring

---

## 🎯 Performance & Comparison

| Aspect | Single-Agent (A) | Multi-Agent (B) |
|--------|------------------|-----------------|
| **Complexity** | Low | Medium |
| **Scalability** | Medium | High |
| **Response Time** | Faster | Slightly slower |
| **API Costs** | Lower | Higher |
| **Best For** | Small datasets | Large, diverse datasets |

**Recommendation**: Multi-Agent (Task B) for real-world deployment with growth potential.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed performance analysis.

---

## 💡 Example Queries

```
"What is the reserved portion for children in Italian inheritance law?"
"How do I file for divorce in Estonia?"
"What are the grounds for contesting a will in Slovenia?"
"Compare divorce waiting periods across Italy, Estonia, and Slovenia"
"What happens if someone dies without a will in Italy?"
```

---

## 🐛 Troubleshooting

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive troubleshooting guide.

**Common issues:**
- OPENAI_API_KEY not found → Check `.env` file
- Vector store not found → Rebuild databases
- 500 errors → Check logs and OpenAI quota
- Slow responses → Reduce `top_k`, optimize context

---

## 👥 Team & Contact

**Project**: Legal RAG System
**Course**: Text Mining / AI Systems
**Submission**: One-shot exam evaluation

For questions or issues, refer to documentation or contact team members.

---

## 📝 License & Acknowledgments

**Dataset**: Contest_Data provided by course instructors
**Frameworks**: LangChain, Streamlit, FastAPI
**Models**: OpenAI (GPT-4o-mini), Hugging Face (sentence-transformers)
**Evaluation**: RAGAS framework

---

## 🚀 Ready for Submission!

**All deliverables completed:**
- ✅ Single-Agent System (Task A)
- ✅ Multi-Agent System (Task B)
- ✅ Chat Interface with JSON logging
- ✅ RAGAS Evaluation Dashboard
- ✅ FastAPI Endpoint
- ✅ Documentation Package (flowcharts, architecture, slides)
- ✅ Internal Test Set (12 questions)
- ✅ Deployment Guide
- ✅ Submission Checklist

**Next steps:**
1. Review [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
2. Run final tests
3. Deploy API endpoint
4. Submit to exam system

**Good luck!** 🎯🚀
