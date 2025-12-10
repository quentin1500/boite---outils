from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session
from .db import init_db, get_session
from .models import Tool, Category, Tag
from . import crud

app = FastAPI(title="Inventaire Outils - API (local)")

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/tools", response_model=dict)
def create_tool(payload: dict, session: Session = Depends(get_session)):
    """
    payload example:
    {
      "name": "Perceuse Bosch",
      "description": "Perceuse sans fil 18V",
      "category_id": 1,
      "tag_names": ["electroportatif","bosch"]
    }
    """
    tag_names = payload.pop("tag_names", None)
    tool = crud.create_tool(session, tool_data=payload, tag_names=tag_names)
    return {"id": tool.id, "name": tool.name}

@app.get("/tools", response_model=List[dict])
def list_tools(q: Optional[str] = Query(None), category_id: Optional[int] = Query(None), tag: Optional[str] = Query(None), limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    tools = crud.search_tools(session, q=q, category_id=category_id, tag=tag, limit=limit, offset=offset)
    out = []
    for t in tools:
        # fetch tags names
        tag_objs = session.exec("SELECT tag.name FROM tag JOIN tooltaglink ON tag.id = tooltaglink.tag_id WHERE tooltaglink.tool_id = :tid", {"tid": t.id}).all()
        tag_names = [r[0] for r in tag_objs] if tag_objs else []
        out.append({"id": t.id, "name": t.name, "description": t.description, "category_id": t.category_id, "tags": tag_names})
    return out

@app.get("/tools/{tool_id}", response_model=dict)
def get_tool(tool_id: int, session: Session = Depends(get_session)):
    t = crud.get_tool(session, tool_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tool not found")
    tag_objs = session.exec("SELECT tag.name FROM tag JOIN tooltaglink ON tag.id = tooltaglink.tag_id WHERE tooltaglink.tool_id = :tid", {"tid": t.id}).all()
    tag_names = [r[0] for r in tag_objs] if tag_objs else []
    return {"id": t.id, "name": t.name, "description": t.description, "category_id": t.category_id, "tags": tag_names}

@app.get("/categories")
def categories(session: Session = Depends(get_session)):
    cats = crud.list_categories(session)
    return [{"id": c.id, "name": c.name} for c in cats]

@app.post("/categories")
def create_category(payload: dict, session: Session = Depends(get_session)):
    c = Category(name=payload.get("name"))
    session.add(c); session.commit(); session.refresh(c)
    return {"id": c.id, "name": c.name}

@app.get("/tags")
def tags(session: Session = Depends(get_session)):
    tags = crud.list_tags(session)
    return [{"id": t.id, "name": t.name} for t in tags]

# simple export csv
@app.get("/export/csv")
def export_csv(session: Session = Depends(get_session)):
    import csv
    from fastapi.responses import StreamingResponse
    tools = session.exec("SELECT id, name, description FROM tool").all()
    def iter_csv():
        writer = csv.writer(__import__("io").StringIO())
        yield "id,name,description\n"
        for r in tools:
            yield f'{r[0]},"{r[1].replace("\"","\'")}", "{(r[2] or "").replace("\"","\'")}"\n'
    return StreamingResponse(iter_csv(), media_type="text/csv")
