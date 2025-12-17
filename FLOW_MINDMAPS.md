# Flow Mind Maps - Text Mining Project

## 1. REACT (STREAMLIT) FLOW

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER ENTRY POINT                            │
│                          streamlit run app.py                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │    app.py      │
                    │  (Home Page)   │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ↓                   ↓                   ↓
┌───────────────┐  ┌────────────────┐  ┌──────────────────┐
│ 1_Settings.py │  │2_Vector_DB     │  │3_Chatbot_QA.py   │
│               │  │  _Builder.py   │  │                  │
│ Configure:    │  │                │  │ Main Query       │
│ • LLM Model   │  │ Build:         │  │ Interface        │
│ • Embeddings  │  │ • FAISS DBs    │  │                  │
│ • JSON Folders│  │ • From JSON    │  │ User Chat        │
│ • Agent Mode  │  │   folders      │  │ ↓                │
│ • Multi-agent │  │                │  │ answer_question()│
│               │  │                │  │ ↓                │
│ Saves to:     │  │ Creates:       │  │ Display Results  │
│ st.session_   │  │ vector_stores/ │  │                  │
│ state.config  │  │ <db_name>/     │  │                  │
└───────┬───────┘  └────────┬───────┘  └────────┬─────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ↓
                ┌───────────────────────┐
                │   RAGConfig Object    │
                │  (backend/config.py)  │
                │                       │
                │ • llm_provider        │
                │ • embedding_provider  │
                │ • json_folders        │
                │ • vector_store_dirs   │
                │ • agentic_mode        │
                │ • use_multiagent      │
                │ • top_k, use_rerank   │
                └───────────┬───────────┘
                            │
                            ↓
                ┌───────────────────────┐
                │  rag_pipeline.py      │
                │  answer_question()    │
                │                       │
                │  ROUTER:              │
                │  if use_hybrid →      │
                │  elif use_multiagent →│
                │  else →               │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐  ┌─────────────────┐  ┌──────────────┐
│ hybrid_rag.py│  │rag_multiagent.py│  │rag_single    │
│              │  │                 │  │  _agent.py   │
│ Legal        │  │ Supervisor +    │  │              │
│ Metadata     │  │ Sub-agents      │  │ Single Agent │
│ Filtering    │  │                 │  │ Processing   │
└──────┬───────┘  └────────┬────────┘  └──────┬───────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ↓
              ┌────────────────────────┐
              │   SHARED COMPONENTS    │
              ├────────────────────────┤
              │ • llm_provider.py      │
              │   LLMBackend.chat()    │
              │                        │
              │ • embeddings.py        │
              │   get_embedding_model()│
              │                        │
              │ • vector_store.py      │
              │   load_vector_store()  │
              │                        │
              │ • rag_utils.py         │
              │   decide_need_retrieval│
              │   decide_relevant_     │
              │   slices()             │
              │   country_gate()       │
              │   retrieve_from_db()   │
              └────────────┬───────────┘
                           │
                           ↓
                   ┌───────────────┐
                   │   RESPONSE    │
                   │               │
                   │ • answer      │
                   │ • docs[]      │
                   │ • reasoning   │
                   │   _trace      │
                   └───────┬───────┘
                           │
                           ↓
                   ┌───────────────┐
                   │3_Chatbot_QA.py│
                   │               │
                   │ Display in UI │
                   │ • Answer      │
                   │ • Sources     │
                   │ • Reasoning   │
                   └───────────────┘
```

## 2. MULTI-AGENT FLOW (Detailed)

```
┌──────────────────────────────────────────────────────────────┐
│                    QUERY INPUT                               │
│          "What are the inheritance laws in Germany?"         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌────────────────────────────────────────────────────────────┐
│  rag_multiagent.py                                         │
│  multiagent_answer_question()                              │
│                                                             │
│  Entry point for multi-agent processing                    │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  _multiagent_answer_question_core()                        │
│                                                             │
│  STEP 1: Initialize Supervisor                             │
│  ┌──────────────────────────────────────┐                  │
│  │ LLMBackend(config)                   │                  │
│  │ - Supervisor agent instance          │                  │
│  │ - Uses configured LLM (OpenAI/HF)    │                  │
│  └──────────────────────────────────────┘                  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 2: Discover Available Vector DBs                     │
│                                                             │
│  ┌──────────────────────────────────────┐                  │
│  │ _get_all_vector_store_dirs()         │                  │
│  │                                      │                  │
│  │ Scans: vector_stores/<db_name>/     │                  │
│  │ Returns: List of DB paths           │                  │
│  └──────────────────────────────────────┘                  │
│                                                             │
│  Example DBs:                                              │
│  • vector_stores/germany_inheritance/                      │
│  • vector_stores/france_divorce/                           │
│  • vector_stores/spain_legal/                              │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 3: Supervisor Decides Which DBs (Future)             │
│                                                             │
│  ┌──────────────────────────────────────┐                  │
│  │ _decide_which_dbs()                  │                  │
│  │                                      │                  │
│  │ Current: Returns ALL DBs             │                  │
│  │ Future: LLM decides relevant DBs     │                  │
│  │ based on query context               │                  │
│  └──────────────────────────────────────┘                  │
│                                                             │
│  Selected DBs: [db1, db2, db3]                             │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 4: Launch Sub-Agents (One per DB)                    │
│                                                             │
│  FOR EACH selected_db:                                     │
│      call subagent_answer_question_with_slices()           │
└────────────────────┬───────────────────────────────────────┘
                     │
         ┌───────────┼───────────┬───────────┐
         │           │           │           │
         ↓           ↓           ↓           ↓
    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │SUB-    │  │SUB-    │  │SUB-    │  │SUB-    │
    │AGENT 1 │  │AGENT 2 │  │AGENT 3 │  │AGENT N │
    │        │  │        │  │        │  │        │
    │DB:     │  │DB:     │  │DB:     │  │DB:     │
    │germany_│  │france_ │  │spain_  │  │...     │
    │inherit │  │divorce │  │legal   │  │        │
    └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  SUB-AGENT PROCESSING                                      │
│  subagent_answer_question_with_slices()                    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase 1: Retrieval Decision                         │  │
│  │ ┌────────────────────────────────────┐              │  │
│  │ │ decide_need_retrieval()            │              │  │
│  │ │                                    │              │  │
│  │ │ • Check for legal keywords        │              │  │
│  │ │ • Ask LLM if DB needed            │              │  │
│  │ │ • Returns: True/False             │              │  │
│  │ └────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                 │
│                          ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase 2: Extract Semantic Slices                    │  │
│  │ ┌────────────────────────────────────┐              │  │
│  │ │ decide_relevant_slices()           │              │  │
│  │ │                                    │              │  │
│  │ │ Query: "inheritance in Germany"    │              │  │
│  │ │ → countries: ["Germany"]          │              │  │
│  │ │ → content_types: ["Inheritance"]  │              │  │
│  │ └────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                 │
│                          ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase 3: Country Validation                         │  │
│  │ ┌────────────────────────────────────┐              │  │
│  │ │ country_gate()                     │              │  │
│  │ │                                    │              │  │
│  │ │ • Check if countries in query     │              │  │
│  │ │   match DB's supported countries  │              │  │
│  │ │ • Filter: Keep only supported     │              │  │
│  │ └────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                 │
│                          ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase 4: Vector Retrieval                           │  │
│  │ ┌────────────────────────────────────┐              │  │
│  │ │ retrieve_from_db()                 │              │  │
│  │ │                                    │              │  │
│  │ │ 1. Load FAISS vector store        │              │  │
│  │ │    via vector_store.py            │              │  │
│  │ │                                    │              │  │
│  │ │ 2. Load embedding model           │              │  │
│  │ │    via embeddings.py              │              │  │
│  │ │                                    │              │  │
│  │ │ 3. Vector similarity search       │              │  │
│  │ │    - Query embedding              │              │  │
│  │ │    - k = top_k * 3                │              │  │
│  │ │                                    │              │  │
│  │ │ 4. Rank & filter documents        │              │  │
│  │ │    - Article prioritization       │              │  │
│  │ │    - Similarity threshold         │              │  │
│  │ │                                    │              │  │
│  │ │ 5. Attach db_name to docs         │              │  │
│  │ └────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                 │
│                          ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Phase 5: Generate Sub-Agent Answer                  │  │
│  │ ┌────────────────────────────────────┐              │  │
│  │ │ LLMBackend.chat()                  │              │  │
│  │ │                                    │              │  │
│  │ │ System Prompt:                     │              │  │
│  │ │ "You are a legal assistant..."     │              │  │
│  │ │                                    │              │  │
│  │ │ User Prompt:                       │              │  │
│  │ │ "Context: <retrieved docs>"        │              │  │
│  │ │ "Question: <user query>"           │              │  │
│  │ │                                    │              │  │
│  │ │ → Sub-agent answer                │              │  │
│  │ └────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                 │
│                          ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Sub-agent Output                                     │  │
│  │ • answer (str)                                       │  │
│  │ • docs (List[Document])                              │  │
│  │ • reasoning_trace (dict)                             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
         ┌───────────┴───────────┬───────────┐
         │                       │           │
         ↓                       ↓           ↓
    ┌─────────┐           ┌─────────┐   ┌─────────┐
    │Answer 1 │           │Answer 2 │   │Answer N │
    │Docs 1   │           │Docs 2   │   │Docs N   │
    └────┬────┘           └────┬────┘   └────┬────┘
         │                     │             │
         └─────────────────────┴─────────────┘
                               │
                               ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 5: Supervisor Synthesis                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Supervisor LLM.chat()                                │  │
│  │                                                       │  │
│  │ System Prompt:                                       │  │
│  │ "You are a supervisor coordinating specialists..."  │  │
│  │                                                       │  │
│  │ User Prompt:                                         │  │
│  │ "Question: <original query>"                         │  │
│  │ "Sub-agent 1 (germany_inherit): <answer1>"          │  │
│  │ "Sub-agent 2 (france_divorce): <answer2>"           │  │
│  │ "..."                                                │  │
│  │                                                       │  │
│  │ Task: Synthesize comprehensive answer               │  │
│  │                                                       │  │
│  │ → Final synthesized answer                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  FINAL OUTPUT                                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ answer: Supervisor's final answer (str)              │  │
│  │                                                       │  │
│  │ docs: Merged documents from all sub-agents          │  │
│  │       [doc1, doc2, doc3, ...]                        │  │
│  │       Each with metadata:                            │  │
│  │       - db_name                                      │  │
│  │       - source                                       │  │
│  │       - country                                      │  │
│  │       - law                                          │  │
│  │                                                       │  │
│  │ reasoning_trace (optional):                          │  │
│  │   {                                                   │  │
│  │     "supervisor_decision": {...},                    │  │
│  │     "sub_agents": [                                  │  │
│  │       {"db": "...", "trace": {...}},                 │  │
│  │       ...                                            │  │
│  │     ]                                                │  │
│  │   }                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ↓
┌────────────────────────────────────────────────────────────┐
│  RETURN TO UI/API                                          │
│                                                             │
│  3_Chatbot_QA.py or api_endpoint.py                        │
│  • Display answer                                          │
│  • Show sources (documents)                                │
│  • Show reasoning trace (if enabled)                       │
└────────────────────────────────────────────────────────────┘
```

## 3. FILE DEPENDENCY MAP

```
┌──────────────────────────────────────────────────────────────┐
│                    CORE CONFIGURATION                        │
│                                                              │
│                    backend/config.py                         │
│                    ┌────────────────┐                        │
│                    │  RAGConfig     │                        │
│                    └────────┬───────┘                        │
│                             │                                │
│         ┌───────────────────┼───────────────────┐            │
└─────────┼───────────────────┼───────────────────┼────────────┘
          │                   │                   │
          ↓                   ↓                   ↓
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ FRONTEND LAYER   │ │  PIPELINE LAYER  │ │  BACKEND LAYER   │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│                  │ │                  │ │                  │
│ app.py           │ │ rag_pipeline.py  │ │ llm_provider.py  │
│   ↓              │ │   (router)       │ │   LLMBackend     │
│ pages/           │ │   ↓              │ │                  │
│ ├─1_Settings.py  │ │   ├─→ rag_      │ │ embeddings.py    │
│ │  (writes       │ │   │   single_   │ │   get_embedding_ │
│ │   config)      │ │   │   agent.py  │ │   model()        │
│ │                │ │   │              │ │                  │
│ ├─2_Vector_DB_   │ │   ├─→ rag_      │ │ vector_store.py  │
│ │  Builder.py    │ │   │   multiagent│ │   build_vector_  │
│ │  (uses vector_ │ │   │   .py       │ │   store()        │
│ │   store.py)    │ │   │              │ │   load_vector_   │
│ │                │ │   │              │ │   store()        │
│ ├─3_Chatbot_QA   │ │   └─→ hybrid_   │ │                  │
│ │  .py           │ │       rag.py    │ │ document_loader  │
│ │  (calls        │ │                  │ │   .py            │
│ │   pipeline)    │ │   All use:       │ │   load_documents│
│ │                │ │   rag_utils.py   │ │   _from_folders()│
│ └──────┬─────────┤ │                  │ │                  │
│        │         │ │                  │ │ rag_utils.py     │
│   API LAYER      │ │                  │ │   (shared        │
│   ↓              │ │                  │ │    utilities)    │
│ api_endpoint.py  │ │                  │ │                  │
│   (FastAPI)      │ │                  │ │                  │
│   ↑              │ │                  │ │                  │
│ run_api.py       │ │                  │ │                  │
│   (CLI runner)   │ │                  │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## 4. DATA FLOW DEPENDENCIES

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                             │
│                                                              │
│  data/                                                      │
│  ├── json_folder_1/                                         │
│  │   ├── law1.json                                         │
│  │   └── law2.json                                         │
│  └── json_folder_2/                                         │
│      └── law3.json                                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
         ┌────────────────────┐
         │ document_loader.py │
         │                    │
         │ load_documents_    │
         │ from_folders()     │
         │                    │
         │ Parses JSON:       │
         │ • Extract content  │
         │ • Preserve metadata│
         │                    │
         │ Returns:           │
         │ List[Document]     │
         └─────────┬──────────┘
                   │
                   ↓
         ┌────────────────────┐
         │  embeddings.py     │
         │                    │
         │  Embedding Model   │
         │  • OpenAI          │
         │  • HuggingFace     │
         └─────────┬──────────┘
                   │
                   ↓
         ┌────────────────────┐
         │ vector_store.py    │
         │                    │
         │ build_vector_store │
         │                    │
         │ Creates FAISS      │
         │ index with         │
         │ embeddings         │
         └─────────┬──────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                 VECTOR DATABASES                            │
│                                                              │
│  vector_stores/                                             │
│  ├── db_name_1/                                             │
│  │   ├── index.faiss                                       │
│  │   └── index.pkl                                         │
│  └── db_name_2/                                             │
│      ├── index.faiss                                        │
│      └── index.pkl                                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
         ┌────────────────────┐
         │   QUERY TIME       │
         │                    │
         │ load_vector_store()│
         │        +           │
         │ similarity_search()│
         │        ↓           │
         │ Retrieved Documents│
         └─────────┬──────────┘
                   │
                   ↓
         ┌────────────────────┐
         │   llm_provider.py  │
         │                    │
         │   LLMBackend.chat()│
         │                    │
         │   Context + Query  │
         │        ↓           │
         │   Generated Answer │
         └────────────────────┘
```

## 5. AGENT COMMUNICATION FLOW

```
MULTI-AGENT ARCHITECTURE:

                    ┌─────────────────────┐
                    │  Supervisor Agent   │
                    │  (LLMBackend)       │
                    │                     │
                    │  Responsibilities:  │
                    │  • Route query      │
                    │  • Coordinate       │
                    │  • Synthesize       │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ↓                           ↓
    ┌────────────────────┐      ┌────────────────────┐
    │  Decision Module   │      │  Synthesis Module  │
    │                    │      │                    │
    │  _decide_which_dbs │      │  Final answer from │
    │                    │      │  all sub-agents    │
    │  Input: Query      │      │                    │
    │  Output: DBs[]     │      │  Combines:         │
    │                    │      │  • Sub-answers     │
    │  Currently: ALL    │      │  • All documents   │
    │  Future: Smart     │      │  • Reasoning trace │
    └─────────┬──────────┘      └────────────────────┘
              │
              │ Dispatches to:
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ↓         ↓         ↓         ↓         ↓
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│SUB-AG 1││SUB-AG 2││SUB-AG 3││SUB-AG 4││SUB-AG N│
│        ││        ││        ││        ││        │
│DB: db1 ││DB: db2 ││DB: db3 ││DB: db4 ││DB: dbN │
│        ││        ││        ││        ││        │
│Process:││        ││        ││        ││        │
│1.Decide││ (Same) ││ (Same) ││ (Same) ││ (Same) │
│  need  ││        ││        ││        ││        │
│2.Slice ││        ││        ││        ││        │
│3.Gate  ││        ││        ││        ││        │
│4.Query ││        ││        ││        ││        │
│5.Answer││        ││        ││        ││        │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
    │         │         │         │         │
    │ Return: │         │         │         │
    │ answer, │         │         │         │
    │ docs,   │         │         │         │
    │ trace   │         │         │         │
    │         │         │         │         │
    └─────────┴─────────┴─────────┴─────────┘
                        │
                        ↓
              ┌──────────────────┐
              │ Supervisor       │
              │ Aggregates       │
              │ All Results      │
              └─────────┬────────┘
                        │
                        ↓
                  Final Answer
```

## 6. SHARED UTILITIES USAGE

```
┌─────────────────────────────────────────────────────────────┐
│                    rag_utils.py                             │
│                  (Shared Functions)                         │
└───────────┬──────────────┬──────────────┬──────────────────┘
            │              │              │
            ↓              ↓              ↓
┌───────────────┐ ┌────────────────┐ ┌──────────────────┐
│ decide_need_  │ │ decide_        │ │ country_gate()   │
│ retrieval()   │ │ relevant_      │ │                  │
│               │ │ slices()       │ │ Validates:       │
│ Checks:       │ │                │ │ extracted        │
│ • Legal       │ │ Extracts from  │ │ countries match  │
│   keywords    │ │ query:         │ │ DB's supported   │
│ • LLM decides │ │ • countries[]  │ │ countries        │
│   if DB needed│ │ • content_     │ │                  │
│               │ │   types[]      │ │ Filters slices   │
│ Returns:      │ │                │ │                  │
│ True/False    │ │ Returns:       │ │ Returns:         │
│               │ │ dict with      │ │ filtered slices  │
│               │ │ slices         │ │                  │
└───────┬───────┘ └────────┬───────┘ └────────┬─────────┘
        │                  │                  │
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ↓
                   ┌───────────────┐
                   │retrieve_from_ │
                   │db()           │
                   │               │
                   │ For each DB:  │
                   │ 1. Load FAISS │
                   │ 2. Embed query│
                   │ 3. Search     │
                   │ 4. Rank       │
                   │ 5. Filter     │
                   │               │
                   │ Returns:      │
                   │ List[Document]│
                   └───────────────┘

Used by:
• rag_single_agent.py
• rag_multiagent.py (sub-agents)
• hybrid_rag.py
```

## 7. COMPLETE QUERY LIFECYCLE

```
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: USER INPUT                                          │
│                                                               │
│ User types query in:                                         │
│ • 3_Chatbot_QA.py (Streamlit UI)                             │
│   OR                                                          │
│ • POST /query to api_endpoint.py (FastAPI)                   │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: CONFIGURATION                                       │
│                                                               │
│ Get RAGConfig from:                                          │
│ • st.session_state (Streamlit)                               │
│   OR                                                          │
│ • config.py get_config() (API)                               │
│                                                               │
│ Config includes:                                             │
│ • LLM provider & model                                       │
│ • Embedding provider & model                                 │
│ • Vector store directories                                   │
│ • Agent mode (standard_rag/hybrid_legal)                     │
│ • Multi-agent flag                                           │
│ • Retrieval settings (top_k, rerank)                         │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 3: ROUTING                                             │
│                                                               │
│ rag_pipeline.py: answer_question()                           │
│                                                               │
│ Decision tree:                                               │
│ IF agentic_mode == "hybrid_legal":                           │
│    → hybrid_answer_question()                                │
│ ELIF use_multiagent == True:                                 │
│    → multiagent_answer_question()                            │
│ ELSE:                                                         │
│    → single_agent_answer_question()                          │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 4: PROCESSING                                          │
│                                                               │
│ Selected agent processes query:                              │
│                                                               │
│ Single-Agent:                                                │
│ • Query all DBs together                                     │
│ • Single retrieval & answer                                  │
│                                                               │
│ Multi-Agent:                                                 │
│ • Supervisor coordinates sub-agents                          │
│ • Each sub-agent queries one DB                              │
│ • Supervisor synthesizes answers                             │
│                                                               │
│ Hybrid:                                                      │
│ • Extract legal metadata from query                          │
│ • Filter by metadata + vector similarity                     │
│ • Single answer with legal context                           │
│                                                               │
│ All use shared utilities:                                    │
│ • decide_need_retrieval()                                    │
│ • decide_relevant_slices()                                   │
│ • country_gate()                                             │
│ • retrieve_from_db()                                         │
│ • LLMBackend.chat()                                          │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 5: RETRIEVAL                                           │
│                                                               │
│ For each vector DB:                                          │
│                                                               │
│ 1. vector_store.py: load_vector_store()                      │
│    • Loads FAISS index.faiss + index.pkl                     │
│                                                               │
│ 2. embeddings.py: get_embedding_model()                      │
│    • Initializes OpenAI or HuggingFace embedder              │
│                                                               │
│ 3. Embed query → vector                                      │
│                                                               │
│ 4. FAISS similarity_search()                                 │
│    • Returns k nearest documents                             │
│                                                               │
│ 5. Rank & filter:                                            │
│    • Similarity threshold                                    │
│    • Article prioritization                                  │
│    • Metadata filtering (hybrid mode)                        │
│                                                               │
│ 6. Attach metadata to documents:                             │
│    • db_name, source, country, law, etc.                     │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 6: ANSWER GENERATION                                   │
│                                                               │
│ llm_provider.py: LLMBackend.chat()                           │
│                                                               │
│ System Prompt:                                               │
│ "You are a helpful legal assistant..."                       │
│                                                               │
│ User Prompt:                                                 │
│ "Context: <retrieved documents>"                             │
│ "Question: <user query>"                                     │
│                                                               │
│ LLM generates:                                               │
│ • Natural language answer                                    │
│ • Citations to source documents                              │
│ • Reasoning (if requested)                                   │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 7: RESPONSE                                            │
│                                                               │
│ Return to caller:                                            │
│                                                               │
│ Tuple: (answer, docs, reasoning_trace)                       │
│                                                               │
│ • answer: str                                                │
│   Final generated answer                                     │
│                                                               │
│ • docs: List[Document]                                       │
│   All retrieved documents with metadata                      │
│                                                               │
│ • reasoning_trace: dict (optional)                           │
│   Logs of decision process                                   │
│   - Retrieval decisions                                      │
│   - Slice extractions                                        │
│   - Country gates                                            │
│   - Sub-agent traces (multi-agent)                           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ PHASE 8: DISPLAY                                             │
│                                                               │
│ Streamlit (3_Chatbot_QA.py):                                 │
│ • Display answer in chat bubble                              │
│ • Show sources in expander                                   │
│ • Show reasoning trace (if enabled)                          │
│ • Save to chat history                                       │
│                                                               │
│ FastAPI (api_endpoint.py):                                   │
│ • Return QueryResponse JSON                                  │
│   {                                                           │
│     "answer": "...",                                         │
│     "contexts": [...],                                       │
│     "source_ids": [...],                                     │
│     "metadata": {...}                                        │
│   }                                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## KEY INSIGHTS

### React (Streamlit) Flow:
1. **Entry**: `app.py` → Multi-page structure
2. **Configuration**: `1_Settings.py` → RAGConfig
3. **Indexing**: `2_Vector_DB_Builder.py` → FAISS creation
4. **Querying**: `3_Chatbot_QA.py` → `answer_question()`
5. **Pipeline**: Routes to appropriate agent
6. **Response**: Display in UI with sources

### Multi-Agent Flow:
1. **Supervisor**: Coordinates multiple specialized agents
2. **DB Selection**: (Future) Smart routing to relevant DBs
3. **Sub-Agents**: One per vector DB, parallel processing
4. **Retrieval**: Each sub-agent queries its DB independently
5. **Synthesis**: Supervisor combines all sub-agent answers
6. **Tracing**: Complete reasoning trace across all agents

### Shared Components:
- **LLM**: Abstracted via `LLMBackend` (OpenAI/HuggingFace)
- **Embeddings**: Pluggable providers
- **Vector Store**: FAISS with caching
- **Utilities**: Reusable decision logic across all agents
- **Configuration**: Centralized RAGConfig dataclass

### Data Flow:
JSON → Documents → Embeddings → FAISS → Query → Retrieval → LLM → Answer
