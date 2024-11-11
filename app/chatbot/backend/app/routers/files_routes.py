from fastapi import APIRouter, HTTPException, File, UploadFile
from ..schemas.response_schema import ResponseSchema
from ..services.chatbot_service import ChatbotService
import os

router = APIRouter()
chatbot_service = ChatbotService()


@router.post("/upload_image/{conversation_id}", summary="Enviar imagem para processamento", description="Envia uma imagem ou PDF, processa o arquivo e resume o conteúdo.")
async def upload_image(conversation_id: str, file: UploadFile = File(...)):
    """
    Faz o upload de uma imagem ou PDF, realiza o processamento e a sumarização do conteúdo.

    Args:
        conversation_id (str): O ID da conversa em que o arquivo será processado.
        file (UploadFile): O arquivo de imagem ou PDF a ser enviado.

    Returns:
        ResponseSchema: A mensagem de resposta após o processamento da imagem ou PDF.

    Raises:
        HTTPException: Se o tipo de arquivo não for suportado ou em caso de erro no processamento.
    """
    if not file.content_type.startswith("image/") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    try:
        temp_path = chatbot_service.save_temp_file(file) if file.content_type != "application/pdf" else chatbot_service.convert_pdf_to_image(file)
        user_message = chatbot_service.transcribe_summarize_and_store_image(conversation_id, temp_path)
        response_message = chatbot_service.get_response(conversation_id, user_message)
        chatbot_service.store_message(conversation_id, user_message, response_message)
        os.remove(temp_path)
        return ResponseSchema(
            status="success",
            message="Image processed successfully",
            data={"response_message": response_message}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_audio/{conversation_id}", summary="Enviar áudio para processamento", description="Envia um arquivo de áudio, processa e resume o conteúdo.")
async def upload_audio(conversation_id: str, file: UploadFile = File(...)):
    """
    Faz o upload de um arquivo de áudio, realiza a conversão, transcrição e sumarização do conteúdo.

    Args:
        conversation_id (str): O ID da conversa em que o arquivo será processado.
        file (UploadFile): O arquivo de áudio a ser enviado.

    Returns:
        ResponseSchema: A mensagem de resposta após o processamento do áudio.

    Raises:
        HTTPException: Se o tipo de arquivo não for suportado ou em caso de erro no processamento.
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    try:
        temp_path = chatbot_service.save_temp_file(file) if file.content_type == "audio/wav" else chatbot_service.convert_to_wav(file)
        user_message = chatbot_service.transcribe_summarize_and_store_audio(conversation_id, temp_path)
        response_message = chatbot_service.get_response(conversation_id, user_message)
        chatbot_service.store_message(conversation_id, user_message, response_message)
        os.remove(temp_path)
        return ResponseSchema(
            status="success",
            message="Audio processed successfully",
            data={"response_message": response_message}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
