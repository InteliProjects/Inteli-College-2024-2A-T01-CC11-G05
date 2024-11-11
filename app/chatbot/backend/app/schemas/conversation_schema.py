from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..schemas.file_summarization_schema import FileSummarizationSchema
from ..schemas.message_schema import MessageSchema
from ..schemas.feedback_schema import FeedbackSchema

# Schema para Conversation
class ConversationSchema(BaseModel):
    """
    Define o schema para uma conversa, representando os campos necessários
    para validação e transformação de dados entre o modelo ORM e a API.
    
    Atributos:
        id (str): ID único da conversa.
        start_time (datetime): Data e hora de início da conversa.
        status (str): Status atual da conversa (ex.: "active", "ended").
        intentions (List[str]): Lista de intenções associadas à conversa.
        user_id (str): ID do usuário associado à conversa.
        end_time (datetime): Data e hora de término da conversa.
        messages (Optional[List[MessageSchema]]): Lista de mensagens na conversa (opcional).
        file_summarizations (Optional[List[FileSummarizationSchema]]): Lista de sumarizações de arquivos associadas à conversa (opcional).
    """
    
    id: str
    start_time: datetime
    status: str
    intentions: List[str] = []
    user_id: str
    end_time: Optional[datetime] = None  
    messages: List[MessageSchema] = []  
    file_summarizations: List[FileSummarizationSchema] = []  

    class Config:
        # Permite converter diretamente de objetos ORM (como SQLAlchemy) para o schema Pydantic
        from_attributes = True
