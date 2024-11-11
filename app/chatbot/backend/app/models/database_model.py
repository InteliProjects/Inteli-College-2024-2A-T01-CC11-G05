from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, ARRAY, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base
from sqlalchemy import Enum as SQLAEnum
import enum


class FileTypeEnum(enum.Enum):
    """Enumeração dos tipos de arquivos suportados."""
    AUDIO = "audio"
    IMAGE = "image"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)

    conversations = relationship("Conversation", back_populates="user")
    """Relacionamento com a tabela de conversas."""


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")  # Estado da conversa (e.g., ativa, encerrada)
    intentions = Column(ARRAY(Text), default=[])  # Intenções identificadas na conversa
    user_id = Column(String, ForeignKey("users.id"))  # Referência ao usuário
    end_time = Column(DateTime, default=None)

    user = relationship("User", back_populates="conversations")
    """Relacionamento com a tabela de usuários."""
    
    messages = relationship("Message", back_populates="conversation")
    """Relacionamento com a tabela de mensagens."""

    file_summarizations = relationship("FileSummarization", back_populates="conversation")
    """Relacionamento com a tabela de sumarizações de arquivos."""


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    user_message = Column(String)
    response_message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    disliked = Column(Boolean, default=False)

    conversation = relationship("Conversation", back_populates="messages")
    """Relacionamento com a tabela de conversas."""


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    rating = Column(Integer)
    comments = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    """Armazena feedback sobre uma conversa."""


class AttendantStatus(Base):
    __tablename__ = "attendant_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Boolean, default=True)  # Disponibilidade do atendente
    updated_at = Column(DateTime, default=datetime.utcnow)
    """Armazena o status do atendente."""


class FileSummarization(Base):
    __tablename__ = "file_summarizations"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    file_type = Column(SQLAEnum(FileTypeEnum), nullable=False)  # Tipo de arquivo (áudio ou imagem)
    summarization = Column(Text, nullable=False)  # Texto da sumarização
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="file_summarizations")
    """Relacionamento com a tabela de conversas."""
