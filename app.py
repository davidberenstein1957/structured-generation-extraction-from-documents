from contextlib import asynccontextmanager
from typing import Annotated

import gradio as gr
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from database.models import Chunk, Document, Relationship
from database.operations import create_db_and_tables, get_session, string_to_uuid4

app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan():
    create_db_and_tables()
    yield


@app.get("/documents/")
async def get_documents(session: SessionDep):
    return {"message": "Hello World"}


@app.get("/documents/{document_id}/")
async def get_document(session: SessionDep, document_id: str) -> Document:
    document = session.get(Document, string_to_uuid4(document_id))
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.post("/documents/process/")
async def process_document(session: SessionDep, file: UploadFile = File(...)):
    """
    Process an uploaded document.
    This is a placeholder endpoint that will be implemented with document processing logic.
    """
    return {"filename": file.filename}


@app.get("/chunks/")
async def get_chunks(session: SessionDep):
    return {"message": "Hello World"}


@app.get("/chunks/{chunk_id}/")
async def get_chunk(session: SessionDep, chunk_id: str) -> Chunk:
    chunk = session.get(Chunk, string_to_uuid4(chunk_id))
    if chunk is None:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return chunk


@app.get("/relationships/")
async def get_relationships(session: SessionDep):
    return {"message": "Hello World"}


@app.get("/relationships/{relationship_id}/")
async def get_relationship(session: SessionDep, relationship_id: str) -> Relationship:
    relationship = session.get(Relationship, string_to_uuid4(relationship_id))
    if relationship is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship


# Create a simple Gradio interface
def greet(name):
    return f"Hello {name}!"


demo = gr.Interface(fn=greet, inputs="text", outputs="text")

# Mount the Gradio app
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app)
