from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum

# Enum para definir o tipo de arquivo
class FileTypeEnum(str, Enum):
    AUDIO = "audio"  
    IMAGE = "image" 

# Schema para sumarização de arquivos
class FileSummarizationSchema(BaseModel):
    """
    Define o schema para a sumarização de arquivos (áudio ou imagem) em uma conversa,
    utilizado para validar e transferir dados entre o ORM e a API.
    
    Atributos:
        id (str): ID único da sumarização.
        conversation_id (str): ID da conversa à qual a sumarização está relacionada.
        file_type (FileTypeEnum): Tipo de arquivo (áudio ou imagem).
        summarization (str): Texto que representa a sumarização do arquivo.
        timestamp (datetime): Data e hora em que a sumarização foi criada.
    """
    
    id: str  
    conversation_id: str  
    file_type: FileTypeEnum  
    summarization: str  
    timestamp: datetime  

    class Config:
        # Permite a conversão direta de objetos ORM para este schema Pydantic
        from_attributes = True
