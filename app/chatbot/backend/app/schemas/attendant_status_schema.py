from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Schema para AttendantStatus
class AttendantStatusSchema(BaseModel):
    """
    Define o schema para o status do atendente, representando os campos necessários 
    para validação e transformação de dados entre o modelo ORM e a API.
    
    Atributos:
        id (Optional[int]): ID do status do atendente. Pode ser opcional.
        name (str): Nome do atendente.
        status (bool): Status atual do atendente (True = disponível, False = indisponível).
        updated_at (datetime): Data e hora da última atualização do status.
    """
    
    id: Optional[int]
    name: str
    status: bool
    updated_at: datetime

    class Config:
        # Indica que o Pydantic pode converter de objetos do SQLAlchemy (ORM) para esse schema
        from_attributes = True
