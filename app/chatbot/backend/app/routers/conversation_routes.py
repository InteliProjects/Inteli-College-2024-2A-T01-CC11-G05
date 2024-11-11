from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..schemas.response_schema import ResponseSchema
from ..services.chatbot_service import ChatbotService
from ..schemas.feedback_schema import FeedbackSchema
from ..schemas.conversation_schema import ConversationSchema

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/start_conversation/{user_id}", summary="Iniciar uma nova conversa", description="Inicia uma nova conversa para um determinado usuário e retorna o ID da conversa e as intenções comuns.")
def start_conversation(user_id: str):
    """
    Inicia uma nova conversa para o usuário especificado e retorna o ID da conversa, além de intenções comuns.

    Args:
        user_id (str): O ID do usuário que está iniciando a conversa.

    Returns:
        ResponseSchema: ID da nova conversa e intenções comuns.

    Raises:
        HTTPException: Em caso de erro ao iniciar a conversa.
    """
    try:
        conversation_id = chatbot_service.start_conversation()
        intentions = chatbot_service.get_most_commom_intentions(user_id)
        return ResponseSchema(
            status="success",
            message="Conversation started",
            data={"conversation_id": conversation_id, "intentions": intentions}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())


@router.post("/end_conversation/{conversation_id}", summary="Encerrar uma conversa", description="Encerra uma conversa ativa.")
def end_conversation(conversation_id: str, background_tasks: BackgroundTasks):
    """
    Encerra a conversa ativa e inicia uma tarefa em segundo plano para processar e armazenar intenções.

    Args:
        conversation_id (str): O ID da conversa que será encerrada.
        background_tasks (BackgroundTasks): Gerenciador de tarefas em segundo plano.

    Returns:
        ResponseSchema: Mensagem confirmando que a conversa foi encerrada.

    Raises:
        HTTPException: Em caso de erro ao encerrar a conversa.
    """
    try:
        chatbot_service.end_conversation(conversation_id)
        background_tasks.add_task(chatbot_service.process_and_store_intentions, conversation_id)

        return ResponseSchema(
            status="success",
            message="Conversation ended"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())


@router.post("/user_feedback", summary="Enviar feedback", description="Envia feedback para uma conversa.")
def user_feedback(feedback: FeedbackSchema):
    """
    Processa o feedback do usuário para uma conversa específica.

    Args:
        feedback (FeedbackSchema): Dados do feedback fornecido pelo usuário.

    Returns:
        ResponseSchema: Mensagem confirmando o recebimento do feedback.

    Raises:
        HTTPException: Em caso de erro ao processar o feedback.
    """
    try:
        chatbot_service.handle_feedback(conversation_id=feedback.conversation_id, rating=feedback.rating, comments=feedback.comments)
        return ResponseSchema(
            status="success",
            message="Feedback received"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())


@router.get("/check_dislikes/{conversation_id}", summary="Verificar dislikes consecutivos", description="Verifica se há três dislikes consecutivos em uma conversa.")
def check_dislikes(conversation_id: str):
    """
    Verifica se a conversa contém três dislikes consecutivos e sugere a intervenção de um atendente.

    Args:
        conversation_id (str): O ID da conversa a ser verificada.

    Returns:
        ResponseSchema: Informação se a intervenção de um atendente deve ser sugerida.

    Raises:
        HTTPException: Em caso de erro ao verificar os dislikes.
    """
    try:
        has_consecutive_dislikes = chatbot_service.check_dislikes(conversation_id)
        suggest_attendant = "True" if has_consecutive_dislikes else "False"
        return ResponseSchema(
            status="success",
            message="Dislike check completed",
            data={"suggest_attendant": suggest_attendant}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())
    

@router.get("/get_conversation/{conversation_id}", summary="Obter detalhes da conversa", description="Busca os detalhes de uma conversa específica.")
def get_conversation(conversation_id: str):
    """
    Recupera os detalhes de uma conversa com base no ID da conversa.

    Args:
        conversation_id (str): O ID da conversa.

    Returns:
        ResponseSchema: Informações da conversa recuperada.

    Raises:
        HTTPException: Se a conversa não for encontrada ou em caso de erro ao buscá-la.
    """
    try:
        conversation = chatbot_service.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail=ResponseSchema(
                status="error",
                message="Conversation not found",
                data={}
            ).json())
        
        conversation_schema = ConversationSchema.from_orm(conversation).dict(exclude_unset=True)

        return ResponseSchema(
            status="success",
            message="Conversation retrieved",
            data={"conversation": conversation_schema}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=ResponseSchema(
            status="error",
            message=str(e),
            data={}
        ).json())
