from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Schema para mensagens em uma conversa
class MessageSchema(BaseModel):
    """
    Define o schema para as mensagens trocadas em uma conversa,
    utilizado para validar e transferir dados entre o ORM e a API.
    
    Atributos:
        id (Optional[int]): ID único da mensagem (opcional, será gerado automaticamente).
        conversation_id (str): ID da conversa à qual a mensagem pertence.
        user_message (str): Mensagem enviada pelo usuário.
        response_message (Optional[str]): Resposta gerada pelo chatbot (opcional).
        timestamp (datetime): Data e hora em que a mensagem foi registrada.
        disliked (bool): Indica se a mensagem foi marcada como "não gostou".
    """
    
    id: Optional[int]  
    conversation_id: str  
    user_message: str 
    response_message: Optional[str]  
    timestamp: datetime  
    disliked: bool  
    
    class Config:
        # Permite a conversão direta de objetos ORM para este schema Pydantic
        from_attributes = True
