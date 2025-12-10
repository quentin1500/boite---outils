from sqlmodel import Session, select
from .models import Tool, Category, Tag, ToolTagLink

def create_tool(session: Session, tool_data: dict, tag_names: list[str] = None):
    tool = Tool(**tool_data)
    session.add(tool)
    session.commit()
    session.refresh(tool)
    if tag_names:
        for name in tag_names:
            tag = session.exec(select(Tag).where(Tag.name == name)).first()
            if not tag:
                tag = Tag(name=name)
                session.add(tag)
                session.commit()
                session.refresh(tag)
            session.add(ToolTagLink(tool_id=tool.id, tag_id=tag.id))
        session.commit()
    session.refresh(tool)
    return tool

def get_tool(session: Session, tool_id: int):
    return session.get(Tool, tool_id)

def search_tools(session: Session, q: str | None = None, category_id: int | None = None, tag: str | None = None, limit=100, offset=0):
    stmt = select(Tool)
    if q:
        stmt = stmt.where(Tool.name.ilike(f"%{q}%"))
    if category_id:
        stmt = stmt.where(Tool.category_id == category_id)
    tools = session.exec(stmt.offset(offset).limit(limit)).all()
    # filter by tag in Python (simple)
    if tag:
        filtered = []
        for t in tools:
            tags = [link.tag_id for link in session.exec(select(ToolTagLink).where(ToolTagLink.tool_id == t.id)).all()]
            if tags:
                # find tag object name
                tag_objs = session.exec(select(Tag).where(Tag.id.in_(tags))).all()
                names = [x.name for x in tag_objs]
                if tag in names:
                    filtered.append(t)
        return filtered
    return tools

def list_categories(session: Session):
    return session.exec(select(Category)).all()

def list_tags(session: Session):
    return session.exec(select(Tag)).all()
