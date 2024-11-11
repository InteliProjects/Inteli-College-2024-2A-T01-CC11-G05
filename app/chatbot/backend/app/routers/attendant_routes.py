from fastapi import APIRouter, HTTPException
from ..schemas.response_schema import ResponseSchema
from ..services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.get("/attendant_status", summary="Obter status do atendente", description="Busca o status do atendente do chatbot (disponível/indisponível)."
)
def attendant_status():
    """
    Recuperar o status atual do atendente do chatbot.

    Returns:
        ResponseSchema: Status da solicitação e disponibilidade atual do atendente do chatbot.
    
    Raises:
        HTTPException: Se ocorrer um erro ao buscar o status.
    """
    try:
        status = chatbot_service.get_attendant_status()
        return ResponseSchema(
            status="success",
            message="Attendant status retrieved successfully",
            data={"status": "Available" if status else "Unavailable"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ResponseSchema(
                status="error",
                message=str(e),
                data={}
            ).json()
        )
