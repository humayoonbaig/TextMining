# Exam Submission Checklist

Use this checklist to ensure everything is ready for your one-shot exam submission.

---

## Pre-Submission Verification

### 1. Core Deliverables ✅

- [ ] **Single-Agent System (Task A)** - Implemented in `backend/rag_single_agent.py`
- [ ] **Multi-Agent System (Task B)** - Implemented in `backend/rag_multiagent.py`
- [ ] **Chat Interface** - Streamlit app with JSON logging
- [ ] **Evaluation Dashboard** - RAGAS metrics in `pages/4_RAG_Evaluation.py`
- [ ] **API Endpoint** - FastAPI server in `backend/api_endpoint.py`

### 2. Documentation Package ✅

- [ ] **Architecture Diagrams** - Flowcharts in `ARCHITECTURE.md`
- [ ] **Architectural Description** - Complete in `ARCHITECTURE.md`
- [ ] **Model Documentation** - Embedding + LLM details in `ARCHITECTURE.md`
- [ ] **Performance Comparison** - Table template in `ARCHITECTURE.md`
- [ ] **Presentation Slides** - 12 slides in `PRESENTATION.md`
- [ ] **Deployment Guide** - Complete in `DEPLOYMENT.md`

### 3. Test Set & Evaluation 📊

- [ ] **Internal Test Set** - 12 questions in `test_set.json`
- [ ] **Ground Truth Answers** - Included in test set
- [ ] **Test Script** - `test_api.py` ready to run
- [ ] **RAGAS Metrics** - Implemented and tested

---

## Technical Verification

### Environment Setup 🔧

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `OPENAI_API_KEY`
- [ ] API key is valid and has credits (check: https://platform.openai.com/usage)

### Data & Vector Databases 📁

- [ ] `Contest_Data/` folder exists with all countries
  - [ ] `Contest_Data/Italy/`
  - [ ] `Contest_Data/Estonia/`
  - [ ] `Contest_Data/slovenia/`
- [ ] Vector databases built in `vector_store/` directory
- [ ] Verified vector DB loads without errors

**To build vector DBs:**
```bash
streamlit run app.py
# Go to Settings → Add data folders → Vector DB Builder → Build
```

### API Server Testing 🚀

- [ ] FastAPI server starts without errors
  ```bash
  python run_api.py
  ```
- [ ] Health check responds successfully
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] System info endpoint works
  ```bash
  curl http://localhost:8000/system_info
  ```
- [ ] Single query endpoint tested
  ```bash
  curl -X POST http://localhost:8000/query \
    -H "Content-Type: application/json" \
    -d '{"question": "What is inheritance law in Italy?", "system": "multi-agent"}'
  ```

### System Behavior Testing 🧪

- [ ] Run automated test suite
  ```bash
  python test_api.py
  ```
- [ ] Single-agent mode returns valid answers
- [ ] Multi-agent mode returns valid answers
- [ ] Both systems include:
  - [ ] Non-empty answer text
  - [ ] List of contexts (retrieved chunks)
  - [ ] List of source IDs
  - [ ] Metadata (num_sources, countries, law types)
- [ ] Response time < 30 seconds per query
- [ ] No errors in logs

### RAGAS Evaluation 📈

- [ ] Created conversations in Streamlit chatbot
- [ ] Saved multiple chat sessions to `chat_sessions.json`
- [ ] Added ground truth labels in evaluation UI
- [ ] Ran RAGAS evaluation successfully
- [ ] All 5 metrics computed:
  - [ ] Context Precision
  - [ ] Context Recall
  - [ ] Faithfulness
  - [ ] Answer Relevancy
  - [ ] Answer Correctness
- [ ] Results documented for presentation

---

## Deployment Preparation

### Server Setup 🌐

- [ ] Server or machine accessible from internet
- [ ] Public IP address obtained
- [ ] Firewall configured to allow port 8000 (or your chosen port)
- [ ] API server running and accessible from external IP
  ```bash
  # From another machine
  curl http://YOUR_PUBLIC_IP:8000/health
  ```

### Production Readiness ⚙️

- [ ] API server runs stably for 30+ minutes without crashes
- [ ] Handles multiple concurrent requests
- [ ] Error handling tested (invalid questions, edge cases)
- [ ] Logging enabled for monitoring
- [ ] Resource usage acceptable (CPU, RAM, disk)

### Backup Plan 💾

- [ ] Have alternative server/deployment option ready
- [ ] Backup of vector databases exists
- [ ] Extra OpenAI API key available (in case of quota issues)
- [ ] Contact information for team members prepared

---

## Submission Information

### Group Information 👥

Prepare the following for submission form:

**Team Member Names:**
- Name 1: _________________________
- Name 2: _________________________
- Name 3: _________________________
- (Add more if needed)

### System Descriptions 📝

**Single-Agent System (Task A) Description:**
```
A ReAct-style unified agent that performs intelligent routing through:
1. Reasoning to decide if retrieval is needed
2. Semantic selection of relevant countries and legal content types
3. Country gate validation to prevent unsupported jurisdiction queries
4. Vector search across all databases with similarity re-ranking
5. Article-aware prioritization when specific codes are mentioned
6. Answer generation using GPT-4o-mini with full source attribution

The system uses sentence-transformers for embeddings and FAISS for vector search.
```

**Multi-Agent System (Task B) Description:**
```
A hierarchical supervisor architecture that coordinates specialized sub-agents:
1. Supervisor agent analyzes the query and routes to relevant database agents
2. Each specialized sub-agent independently performs ReAct-style reasoning and retrieval from its designated vector database (per country/jurisdiction)
3. Sub-agents return partial answers with retrieved sources
4. Supervisor synthesizes a coherent final answer, resolving any conflicts
5. Enables parallel retrieval and jurisdiction-specific expertise

Uses the same embedding and LLM models as Task A, with enhanced orchestration.
```

### Application Endpoint 🔗

**Endpoint URL Format:**
```
http://YOUR_PUBLIC_IP:8000/query
```

**Example:**
```
http://123.45.67.89:8000/query
```

**If using a domain:**
```
https://legal-rag.yourdomain.com/query
```

**Verify this exact URL works:**
```bash
curl -X POST http://YOUR_PUBLIC_IP:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Test question", "system": "multi-agent"}'
```

---

## Final Pre-Submission Checks

### 24 Hours Before Submission ⏰

- [ ] Run full system test with all 12 test questions
- [ ] Verify average response time is acceptable
- [ ] Check OpenAI account has sufficient credits
  - Estimate: 10 questions × 5 LLM calls each × $0.0005/call ≈ $0.025
  - Have at least $5 available for safety margin
- [ ] Confirm server uptime and stability
- [ ] Test from external network (not localhost)

### 1 Hour Before Submission ⚰️

- [ ] Restart API server with fresh logs
  ```bash
  python run_api.py --host 0.0.0.0 --port 8000 > api.log 2>&1 &
  ```
- [ ] Monitor logs to ensure no errors
- [ ] Test endpoint one final time
- [ ] Verify internet connection is stable
- [ ] Have team members on standby for troubleshooting

### During Submission ⚡

- [ ] Keep terminal/server window visible
- [ ] Monitor logs in real-time
  ```bash
  tail -f api.log
  ```
- [ ] Do NOT restart or modify anything
- [ ] Note exact time of submission
- [ ] Keep screenshot of successful health check

### After Submission 📊

- [ ] Keep server running for at least 30 minutes
- [ ] Save all logs
- [ ] Document any issues encountered
- [ ] Wait for official evaluation results
- [ ] Celebrate completion! 🎉

---

## Emergency Contacts

**If something goes wrong:**

1. **OpenAI API Issues:**
   - Check status: https://status.openai.com/
   - Verify API key: https://platform.openai.com/api-keys
   - Check usage: https://platform.openai.com/usage

2. **Server Issues:**
   - Restart API server
   - Check firewall settings
   - Verify port availability
   - Test from different network

3. **Code Issues:**
   - Check `api.log` for detailed errors
   - Verify vector databases exist
   - Confirm `.env` file is loaded
   - Test with simpler question first

---

## Success Criteria Verification

Before submitting, ensure your system:

✅ **Accepts POST requests** to `/query` endpoint
✅ **Returns JSON** with required fields:
   - `question` (string)
   - `answer` (string)
   - `contexts` (list of strings)
   - `source_ids` (list of strings)
   - `metadata` (object)
✅ **Responds within timeout** (< 60 seconds recommended)
✅ **Handles various question types**:
   - Single country queries
   - Multi-country comparative queries
   - Inheritance vs Divorce questions
   - Specific article references
✅ **Provides accurate answers** grounded in sources
✅ **Returns non-empty contexts** from vector retrieval
✅ **Includes proper metadata** (countries, law types)

---

## Post-Evaluation

After receiving official results:

- [ ] Compare with internal RAGAS metrics
- [ ] Document actual performance vs expected
- [ ] Identify areas for improvement
- [ ] Update documentation with lessons learned
- [ ] Archive submission version
- [ ] Plan next iteration

---

## Quick Command Reference

```bash
# Start API server (multi-agent)
python run_api.py

# Start API server (single-agent)
python run_api.py --single-agent

# Run test suite
python test_api.py --url http://localhost:8000

# Build vector databases
streamlit run app.py
# Then: Settings → Vector DB Builder

# Check health
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here", "system": "multi-agent"}'

# Monitor logs
tail -f api.log
```

---

## Final Reminder

⚠️ **This is a ONE-SHOT submission - you cannot retry!**

Take your time to verify everything works before submitting.

**Good luck!** 🚀🎯
