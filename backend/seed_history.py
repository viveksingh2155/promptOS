from sqlalchemy import create_engine, text
import uuid, datetime

engine = create_engine("sqlite:///promptos.db")
with engine.connect() as conn:

    # --- Delete last 8 ---
    rows = conn.execute(text("SELECT id FROM prompt_history ORDER BY created_at DESC LIMIT 8")).fetchall()
    if rows:
        ids = [r[0] for r in rows]
        for rid in ids:
            conn.execute(text("DELETE FROM prompt_history WHERE id = :id"), {"id": rid})
        conn.commit()
    print(f"Deleted {len(rows)} entries.")

    # --- Insert 4 demo entries ---
    demos = [
        {
            "id": str(uuid.uuid4()),
            "title": "Build a REST API with authentication and rate limiting...",
            "original_prompt": "make a rest api that has login and also limits how many requests people can make",
            "optimized_prompt": "**Role:** You are a senior backend engineer specializing in secure API design.\n\n**Task:** Design and implement a production-ready REST API with JWT-based authentication, refresh token rotation, and a sliding window rate limiter (100 req/min per user).\n\n**Requirements:**\n- FastAPI or Express.js with TypeScript\n- OpenAPI/Swagger documentation\n- RBAC for endpoint authorization\n- Standardized error responses and request logging\n\n**Output Format:** Full project structure, core implementation files, and a README with setup instructions.",
            "score": 91,
            "clarity_score": 93,
            "context_score": 89,
            "token_count": 142,
            "model": "llama3.1",
            "format": "GPT",
            "latency": 47230.0,
            "has_hallucination_risk": 0,
            "created_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Write a machine learning pipeline for image classification...",
            "original_prompt": "i want to classify images using ml like cats vs dogs or something with training",
            "optimized_prompt": "**Role:** You are an expert ML engineer with deep expertise in computer vision.\n\n**Task:** Build a complete binary image classification pipeline (cats vs. dogs) using transfer learning with PyTorch and a pretrained ResNet-50 backbone.\n\n**Requirements:**\n- Data augmentation: random flips, rotations, color jitter\n- Training loop with early stopping, LR scheduler, and checkpoint saving\n- Metrics: accuracy, precision, recall, F1, confusion matrix\n\n**Output Format:** Modular Python scripts (dataset.py, model.py, train.py, evaluate.py) with inline comments.",
            "score": 88,
            "clarity_score": 90,
            "context_score": 86,
            "token_count": 127,
            "model": "llama3.1",
            "format": "GPT",
            "latency": 52100.0,
            "has_hallucination_risk": 0,
            "created_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Create a Next.js dashboard with real-time data and dark mode...",
            "original_prompt": "build a dashboard in nextjs with charts and real time updates and dark mode toggle",
            "optimized_prompt": "**Role:** You are a senior frontend engineer specializing in React and Next.js data visualization.\n\n**Task:** Build a responsive admin dashboard in Next.js 14 (App Router) with real-time SSE data updates, Recharts visualizations (line, bar, donut), and a dark/light mode toggle with localStorage persistence.\n\n**Requirements:**\n- TypeScript throughout\n- Zustand for global state\n- Tailwind CSS with CSS variable theming\n- Skeleton loading states for all data components\n\n**Output Format:** Full component tree, page layout, and a mock data service simulating real-time feeds.",
            "score": 94,
            "clarity_score": 96,
            "context_score": 92,
            "token_count": 158,
            "model": "llama3.1",
            "format": "GPT",
            "latency": 44870.0,
            "has_hallucination_risk": 0,
            "created_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Write a technical blog post about microservices architecture...",
            "original_prompt": "write a blog post about microservices and why they are good or bad and when to use them",
            "optimized_prompt": "**Role:** You are a staff engineer and technical writer with 10+ years of distributed systems experience.\n\n**Task:** Write a 1500-2000 word technical blog post titled 'Microservices in 2025: When They Shine and When They Sink'.\n\n**Structure:** Intro, core benefits, hidden costs, decision framework (monolith-first vs microservices-first), real-world case studies (Uber, Netflix), actionable conclusion.\n\n**Requirements:**\n- Cite concrete metrics where possible\n- Balanced and opinionated tone\n- Avoid marketing language\n\n**Output Format:** Full markdown article ready for Dev.to or Hashnode.",
            "score": 86,
            "clarity_score": 88,
            "context_score": 84,
            "token_count": 171,
            "model": "llama3.1",
            "format": "Claude",
            "latency": 39540.0,
            "has_hallucination_risk": 0,
            "created_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=20)).isoformat(),
        },
    ]

    for d in demos:
        conn.execute(text("""
            INSERT INTO prompt_history
                (id, title, original_prompt, optimized_prompt, score, clarity_score, context_score,
                 token_count, model, format, latency, has_hallucination_risk, created_at)
            VALUES
                (:id, :title, :original_prompt, :optimized_prompt, :score, :clarity_score, :context_score,
                 :token_count, :model, :format, :latency, :has_hallucination_risk, :created_at)
        """), d)
    conn.commit()
    print(f"Inserted {len(demos)} demo entries.")

    total = conn.execute(text("SELECT COUNT(*) FROM prompt_history")).scalar()
    print(f"Total entries now: {total}")
