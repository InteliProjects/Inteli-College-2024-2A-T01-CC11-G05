from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Schema para Feedback
class FeedbackSchema(BaseModel):
    """
    Define o schema para o feedback de uma conversa, usado para validar e 
    transferir dados entre o ORM e a API.
    
    Atributos:
        id (Optional[int]): ID único do feedback (opcional, geralmente preenchido pelo banco de dados).
        conversation_id (str): ID da conversa à qual o feedback está relacionado.
        rating (int): Avaliação dada pelo usuário (ex.: de 1 a 5).
        comments (Optional[str]): Comentários adicionais fornecidos pelo usuário (opcional).
        timestamp (datetime): Data e hora em que o feedback foi enviado.
    """
    
    id: Optional[int]  
    conversation_id: str  
    rating: int  
    comments: Optional[str] 
    timestamp: datetime  

    class Config:
        # Permite a conversão direta de objetos ORM para este schema Pydantic
        from_attributes = True
