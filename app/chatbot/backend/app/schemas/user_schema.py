from pydantic import BaseModel

# Schema para o usuário
class UserSchema(BaseModel):
    """
    Define o schema para o usuário, utilizado para representar as informações do usuário na API.
    
    Atributos:
        id (str): Identificador único do usuário.
        name (str): Nome do usuário.
    """
    
    id: str  
    name: str  

    class Config:
        # Permite a conversão direta de objetos ORM para este schema Pydantic
        from_attributes = True
