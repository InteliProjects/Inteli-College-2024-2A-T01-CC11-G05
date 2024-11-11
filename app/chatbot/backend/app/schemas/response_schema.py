from pydantic import BaseModel
from typing import Any, Dict, Optional

# Schema para respostas da API
class ResponseSchema(BaseModel):
    """
    Define o schema para a estrutura das respostas da API,
    utilizado para padronizar a resposta das rotas da API.
    
    Atributos:
        status (str): Status da resposta, indicando se a operação foi bem-sucedida ou se houve um erro.
        message (str): Mensagem explicativa sobre o resultado da operação.
        data (Optional[Any]): Dados adicionais retornados pela operação (opcional).
    """
    
    status: str  
    message: str  
    data: Optional[Any] = {}  

    class Config:
        # Permite a conversão direta de objetos ORM para este schema Pydantic
        from_attributes = True
