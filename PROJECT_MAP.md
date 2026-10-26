# 🗺️ PromptOS — Project Architecture Map

> **Auto-generated documentation. Inspection-only — no files were modified or deleted.**

---

## 📦 Technology & Framework Stack

| Layer              | Technology       | Version  | Purpose                                     |
|--------------------|-----------------|----------|---------------------------------------------|
| Backend Runtime    | Python           | 3.12     | Server-side logic                            |
| Backend Framework  | FastAPI          | 0.162.0  | REST API with async support                  |
| ORM                | SQLAlchemy       | 2.1.6    | Database models & queries                    |
| Validation         | Pydantic         | 2.14.1   | Request/response schemas                     |
| LLM Engine         | Ollama           | 0.6.3    | Local LLM inference (Gemma3 / Llama3.1)      |
| Streaming          | SSE-Starlette    | 3.5.1    | Server-Sent Events for real-time updates     |
| Language Detection | langdetect       | 1.0.9    | Multi-language prompt detection              |
| Database           | SQLite           | —        | Lightweight file-based storage               |
| Frontend Runtime   | Node.js          | 18+      | JavaScript runtime                           |
| Frontend Framework | Next.js          | 16.2.4   | React meta-framework (App Router)            |
| UI Library         | React            | 19.2.4   | Component-based UI                           |
| Styling            | Tailwind CSS     | 4.x      | Utility-first CSS framework                  |
| State Management   | Zustand          | 5.0.12   | Lightweight global store                     |
| Animations         | Framer Motion    | 12.38.0  | Smooth UI transitions & micro-animations     |
| Icons              | Lucide React     | 1.8.0    | SVG icon library                             |
| Auth               | NextAuth.js      | 4.24.14  | Authentication (Google OAuth)                |

---

## 🏗️ Architecture Overview

PromptOS runs a **4-agent prompt optimization pipeline**, where each agent is a specialized LLM call via Ollama:

```
User Input ──▶ [🧹 Cleaner] ──▶ [🔍 Analyzer] ──▶ [🏗️ Builder] ──▶ [✨ Optimizer] ──▶ Optimized Output + Score
```

| Agent       | File                    | Role                                              |
|-------------|------------------------|----------------------------------------------------|
| Cleaner     | `pipeline/cleaner.py`  | Strips noise, fixes grammar, normalizes input       |
| Analyzer    | `pipeline/analyzer.py` | Extracts intent, context, and requirements          |
| Builder     | `pipeline/builder.py`  | Structures prompt into target format (GPT/Claude)   |
| Optimizer   | `pipeline/optimizer.py`| Final polish — clarity, constraints, scoring        |
| Language    | `pipeline/language.py` | Detects input language (20+ langs + Hinglish)       |

---

## 📁 Complete Directory Tree

```
promptOS/
│
├── README.md                            # Project documentation & setup guide
├── PROJECT_MAP.md                       # ← This file
├── .git/                                # Git version control history
├── .venv/                               # Python virtual environment (active)
├── .vscode/
│   └── settings.json                    # VS Code workspace settings
│
├── crop.py                              # One-off image cropping utility script
├── diagnostics.py                       # System health checker (Ollama, ports, envs)
├── h                                    # Accidental git log output (junk file)
├── promptos.db                          # Stale copy of backend/promptos.db
│
│
├── backend/                             # ═══ FASTAPI BACKEND ═══════════════════
│   │
│   ├── main.py                          # 🚀 Entry point — FastAPI app, CORS, routers
│   ├── database.py                      # 🗄️  SQLAlchemy engine, sessions, migrations
│   ├── models.py                        # 📐 ORM models (PromptHistory table)
│   ├── schemas.py                       # 📋 Pydantic request/response schemas
│   ├── requirements.txt                 # 📦 Python dependencies (10 packages)
│   ├── promptos.db                      # 💾 SQLite database file (active)
│   │
│   ├── pipeline/                        # ── 4-Agent Optimization Pipeline ──────
│   │   ├── cleaner.py                   #    Agent 1 → Input sanitization & grammar
│   │   ├── analyzer.py                  #    Agent 2 → Intent & context extraction
│   │   ├── builder.py                   #    Agent 3 → Structured prompt construction
│   │   ├── optimizer.py                 #    Agent 4 → Final optimization & scoring
│   │   └── language.py                  #    Language detection (Unicode + Hinglish)
│   │
│   ├── routers/                         # ── API Route Handlers ─────────────────
│   │   ├── optimizer.py                 #    POST /api/optimize (SSE streaming)
│   │   ├── history.py                   #    GET/DELETE /api/history (CRUD)
│   │   └── templates.py                 #    GET /api/templates (presets)
│   │
│   ├── tests/                           # ── Test Suite ─────────────────────────
│   │   └── test_multilingual_pipeline.py#    Multi-language detection tests
│   │
│   ├── delete_history.py                # 🔧 Utility: prune DB to 3 oldest records
│   └── seed_history.py                  # 🔧 Utility: insert demo history entries
│
│
├── frontend/                            # ═══ NEXT.JS FRONTEND ══════════════════
│   │
│   │── package.json                     # 📦 Node dependencies & npm scripts
│   │── package-lock.json                # 🔒 Dependency lockfile (238 KB)
│   │── tsconfig.json                    # ⚙️  TypeScript compiler config
│   │── next.config.ts                   # ⚙️  Next.js framework config
│   │── next-env.d.ts                    # ⚙️  Next.js TypeScript declarations
│   │── tailwind.config.ts               # 🎨 Tailwind CSS theme & customizations
│   │── postcss.config.mjs               # ⚙️  PostCSS plugin config
│   │── eslint.config.mjs                # ⚙️  ESLint linting rules
│   │── .env.local                       # 🔑 Environment vars (OAuth secrets)
│   │── .gitignore                       # 🚫 Git ignore rules
│   │── auth.ts                          # 🔐 NextAuth.js config (Google OAuth)
│   │── AGENTS.md                        # 📝 AI agent behavior rules
│   │── CLAUDE.md                        # 📝 Placeholder file
│   │── README.md                        # 📖 Frontend-specific docs
│   │
│   ├── app/                             # ── Next.js App Router (Pages) ─────────
│   │   ├── layout.tsx                   #    Root layout — HTML shell, fonts
│   │   ├── page.tsx                     #    🏠 Home — main prompt workspace
│   │   ├── globals.css                  #    🎨 Global styles (20 KB)
│   │   ├── favicon.ico                  #    🌐 Browser tab icon
│   │   │
│   │   ├── history/
│   │   │   └── page.tsx                 #    📜 History — past optimized prompts
│   │   ├── settings/
│   │   │   └── page.tsx                 #    ⚙️  Settings — model & format prefs
│   │   ├── templates/
│   │   │   └── page.tsx                 #    📋 Templates — preset prompts
│   │   ├── workspace/                   #    (empty directory)
│   │   │
│   │   └── api/auth/
│   │       └── [...nextauth]/
│   │           └── route.ts             #    🔐 NextAuth catch-all API route
│   │
│   ├── components/                      # ── React Components ───────────────────
│   │   │
│   │   ├── auth/
│   │   │   └── LoginPage.tsx            #    🔐 Login UI with Google OAuth
│   │   │
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx            #    📐 Main app shell (sidebar + content)
│   │   │   ├── Navbar.tsx               #    🧭 Top navigation bar
│   │   │   └── Sidebar.tsx              #    📂 Left sidebar with nav links
│   │   │
│   │   ├── workspace/
│   │   │   ├── PromptInput.tsx          #    ✏️  Prompt text area + controls
│   │   │   ├── ProcessingState.tsx      #    ⏳ Pipeline progress animation
│   │   │   ├── PipelineView.tsx         #    🔄 Visual pipeline step tracker
│   │   │   ├── OutputDisplay.tsx        #    📄 Optimized output + copy/export
│   │   │   ├── PromptScore.tsx          #    📊 Quality score gauges
│   │   │   ├── TokenUsage.tsx           #    🔢 Token count visualization
│   │   │   └── HintCards.tsx            #    💡 Contextual prompt tips
│   │   │
│   │   ├── history/                     #    (empty — placeholder)
│   │   ├── settings/                    #    (empty — placeholder)
│   │   └── templates/                   #    (empty — placeholder)
│   │
│   ├── lib/                             # ── Shared Utilities ───────────────────
│   │   ├── api.ts                       #    🌐 HTTP/SSE client for backend calls
│   │   └── utils.ts                     #    🔧 Helpers: cn(), formatDate(), etc.
│   │
│   ├── store/
│   │   └── useStore.ts                  #    🏪 Zustand global state management
│   │
│   ├── types/
│   │   └── index.ts                     #    📝 TypeScript interfaces & types
│   │
│   ├── public/                          # ── Static Assets ──────────────────────
│   │   ├── logo.png                     #    🖼️  PromptOS logo (72 KB)
│   │   ├── file.svg                     #    Next.js boilerplate icon
│   │   ├── globe.svg                    #    Next.js boilerplate icon
│   │   ├── next.svg                     #    Next.js boilerplate icon
│   │   ├── vercel.svg                   #    Vercel boilerplate icon
│   │   └── window.svg                   #    Next.js boilerplate icon
│   │
│   ├── node_modules/                    #    📦 Installed npm packages
│   └── .next/                           #    Build cache (auto-regenerated)
```

---

## 📊 File Count Summary

| Area         | Source Files         | Config Files | Other              |
|--------------|---------------------|--------------|--------------------|
| **Backend**  | 10 `.py` files       | 1            | 1 DB, 1 test       |
| **Frontend** | 18 `.tsx`/`.ts` files| 7            | 6 static assets    |
| **Root**     | 2 utility `.py`      | 1 README     | 2 junk files       |
| **Total**    | **30 source files**  | **9 configs**| —                  |

---

## 🔗 API Endpoints

| Method   | Endpoint            | Handler                  | Description                          |
|----------|---------------------|--------------------------|--------------------------------------|
| `GET`    | `/health`           | `main.py`                | Health check                         |
| `POST`   | `/api/optimize`     | `routers/optimizer.py`   | Run 4-agent pipeline (SSE stream)    |
| `GET`    | `/api/history`      | `routers/history.py`     | List all prompt history              |
| `DELETE` | `/api/history/{id}` | `routers/history.py`     | Delete a history entry               |
| `GET`    | `/api/templates`    | `routers/templates.py`   | Get preset prompt templates          |

---

## 🚀 How to Run

```bash
# Terminal 1 — Backend (FastAPI on :8000)
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend (Next.js on :3000)
cd frontend
npm run dev
```

| Service   | URL                        |
|-----------|----------------------------|
| Frontend  | http://localhost:3000       |
| Backend   | http://localhost:8000       |
| API Docs  | http://localhost:8000/docs  |
