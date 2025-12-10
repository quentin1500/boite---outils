from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class ToolTagLink(SQLModel, table=True):
    tool_id: int | None = Field(default=None, foreign_key="tool.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)



class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    tools: list[Tool] = Relationship(
        back_populates="tags",
        link_model=ToolTagLink
    )

class ToolBase(SQLModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    photo_path: Optional[str] = None

class Tool(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None

    tags: list["Tag"] = Relationship(
        back_populates="tools",
        link_model=ToolTagLink
    )

Tag.tools = Relationship(back_populates="tags", link_model=ToolTagLink)
