import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from schemas import TemplateOut

router = APIRouter()

SEED_TEMPLATES = [
    {
        "id": str(uuid.uuid4()), "title": "Refactoring Agent", "category": "coding",
        "description": "A structured prompt to analyze legacy code and suggest modern alternatives.",
        "icon": "🔧",
        "prompt_text": "Act as a Senior Software Engineer. Review the following code block. Identify areas of technical debt, suggest modern refactoring approaches, and provide concrete code examples.",
        "preview_text": "Act as a Senior Software Engineer. Review the following code block. Identify...",
    },
    {
        "id": str(uuid.uuid4()), "title": "SEO Blog Post", "category": "writing",
        "description": "Generates a highly structured, SEO-optimized blog article with hooks.",
        "icon": "✍️",
        "prompt_text": "Write a comprehensive blog post about [TOPIC]. Target audience is [AUDIENCE]. Include SEO keywords naturally. Structure: Hook → Problem → Solution → Examples → CTA.",
        "preview_text": "Write a comprehensive blog post about [TOPIC]. Target audience is [AUDIENCE]...",
    }
]

def seed_templates(db: Session):
    count = db.query(models.Template).count()
    if count == 0:
        for t in SEED_TEMPLATES:
            db_template = models.Template(
                id=t["id"], title=t["title"], category=t["category"],
                description=t["description"], icon=t["icon"],
                prompt_text=t["prompt_text"], preview_text=t["preview_text"],
            )
            db.add(db_template)
        db.commit()

@router.get("/templates", response_model=List[TemplateOut])
def get_templates(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    seed_templates(db)
    query = db.query(models.Template)
    if category and category != "all":
        query = query.filter(models.Template.category == category)
    templates = query.all()
    return [
        TemplateOut(
            id=t.id, title=t.title, description=t.description, category=t.category,
            promptText=t.prompt_text, icon=t.icon, previewText=t.preview_text,
        )
        for t in templates
    ]
