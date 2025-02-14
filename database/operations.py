import hashlib
from uuid import UUID

from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def string_to_uuid4(text: str) -> UUID:
    """Convert a string to a deterministic UUID4 by hashing it."""
    # Create SHA-256 hash of the text
    hash_obj = hashlib.sha256(text.encode())
    # Get first 16 bytes (128 bits) of hash
    hash_bytes = hash_obj.digest()[:16]
    # Set version to 4 and variant to RFC 4122
    hash_bytes = bytearray(hash_bytes)
    hash_bytes[6] = (hash_bytes[6] & 0x0F) | 0x40
    hash_bytes[8] = (hash_bytes[8] & 0x3F) | 0x80
    return UUID(bytes=bytes(hash_bytes))
