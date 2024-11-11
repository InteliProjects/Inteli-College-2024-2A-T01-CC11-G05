from fastapi import APIRouter, HTTPException
from ..schemas.response_schema import ResponseSchema
from ..services.chatbot_service import ChatbotService
from ..schemas.message_schema import MessageSchema
from ..schemas.conversation_schema import ConversationSchema
from pydantic import BaseModel

router = APIRouter()
chatbot_service = ChatbotService()

class MessageRequest(BaseModel):
    user_message: str

@router.post("/send_message/{conversation_id}", summary="Enviar mensagem do usuário", description="Envia uma mensagem do usuário para o chatbot e recebe uma resposta.")
def send_message(conversation_id: str, message: MessageRequest):
    """
    Envia uma mensagem do usuário para o chatbot, obtém a resposta gerada e armazena ambas as mensagens na conversa.

    Args:
        conversation_id (str): O ID da conversa.
        message (MessageRequest): O objeto contendo a mensagem do usuário.

    Returns:
        ResponseSchema: Status da solicitação e a resposta gerada pelo chatbot.

    Raises:
        HTTPException: Em caso de erro durante o envio da mensagem ou ao gerar a resposta.
    """
    try:
        response_message = chatbot_service.get_response(conversation_id, message.user_message)
        chatbot_service.store_message(conversation_id, message.user_message, response_message)
        return ResponseSchema(
            status="success",
            message="Message sent and response received",
            data={"response": response_message}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())


@router.patch("/dislike_message/{conversation_id}/{message_id}", summary="Descurtir mensagem", description="Registra uma 'descurtida' para uma mensagem específica em uma conversa.")
def dislike_message(message_id: int, conversation_id: str):
    """
    Registra a descurtida de uma mensagem em uma conversa, marcando a mensagem como "disliked".

    Args:
        message_id (int): O ID da mensagem que será marcada como descurtida.
        conversation_id (str): O ID da conversa associada à mensagem.

    Returns:
        ResponseSchema: Status da solicitação confirmando que a descurtida foi registrada.

    Raises:
        HTTPException: Em caso de erro ao tentar registrar a descurtida.
    """
    try:
        chatbot_service.dislike_message(message_id, conversation_id)
        return ResponseSchema(
            status="success",
            message="Dislike recorded"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())
