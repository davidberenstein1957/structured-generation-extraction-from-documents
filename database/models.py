from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    path: str


class Chunk(SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    document_id: UUID = Field(foreign_key="document.id")
    text: str


class Relationship(SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    chunk_id: UUID = Field(foreign_key="chunk.id")
    from_entity: str = Field(default="")
    from_entity_type: str = Field(default="")
    to_entity: str = Field(default="")
    to_entity_type: str = Field(default="")
    relation: str = Field(default="")
