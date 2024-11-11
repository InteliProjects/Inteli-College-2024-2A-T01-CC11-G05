from http.client import HTTPException
from ..models.chatbot_model import ChatbotModel
from app.database.config.db import SessionLocal
from ..models.database_model import Message, Feedback, Conversation
from ..utils import db_utils  
from pdf2image import convert_from_path
from PIL import Image
from fastapi import UploadFile, HTTPException
from pydub import AudioSegment
import os


class ChatbotService:
    def __init__(self):
        self.model = ChatbotModel()

    def get_response(self, conversation_id: str, user_input: str) -> str:
        """
        Obtém a resposta do chatbot com base no histórico da conversa e na entrada do usuário.

        Args:
            conversation_id (str): Identificador da conversa.
            user_input (str): Mensagem do usuário.

        Returns:
            str: Resposta gerada pelo chatbot.
        """
        db_session = SessionLocal()
        messages = db_utils.get_messages_for_conversation(db_session, conversation_id)

        sentiment = self.model.analyze_sentiment(user_input)
        
        db_session.close()
        response = self.model.generate_response(messages, user_input, sentiment)
        return response

    def start_conversation(self) -> str:
        """
        Inicia uma nova conversa e retorna o identificador da conversa.

        Returns:
            str: Identificador da nova conversa.
        """
        db_session = SessionLocal()
        conversation_id = db_utils.start_new_conversation(db_session)
        db_session.close()
        return conversation_id

    def store_message(self, conversation_id: str, user_message: str, response_message: str):
        """
        Armazena uma mensagem e a resposta associada no banco de dados.

        Args:
            conversation_id (str): Identificador da conversa.
            user_message (str): Mensagem do usuário.
            response_message (str): Resposta gerada pelo chatbot.
        """
        db_session = SessionLocal()
        db_utils.store_message(db_session, conversation_id, user_message, response_message)
        db_session.close()

    def dislike_message(self, message_id: int, conversation_id: str):
        """
        Registra um desagrado para uma mensagem específica.

        Args:
            message_id (int): Identificador da mensagem.
            conversation_id (str): Identificador da conversa.
        """
        db_session = SessionLocal()
        db_utils.record_dislike(db_session, message_id, conversation_id)
        db_session.close()

    def check_dislikes(self, conversation_id: str) -> bool:
        """
        Verifica se há três desagrados consecutivos em uma conversa.

        Args:
            conversation_id (str): Identificador da conversa.

        Returns:
            bool: True se houver três desagrados consecutivos, False caso contrário.
        """
        db_session = SessionLocal()
        result = self.model.check_consecutive_dislikes(db_session, conversation_id)
        db_session.close()
        return result

    def get_conversation(self, conversation_id: str):
        """
        Obtém o histórico de uma conversa específica.

        Args:
            conversation_id (str): Identificador da conversa.

        Returns:
            Conversation: Objeto de conversa com o histórico.
        """
        db_session = SessionLocal()
        conversation = db_utils.get_conversation_history(db_session, conversation_id)
        db_session.close()
        return conversation

    def get_most_commom_intentions(self, user_id: str):
        """
        Obtém as intenções mais comuns para um usuário específico.

        Args:
            user_id (str): Identificador do usuário.

        Returns:
            List[str]: Lista de intenções mais comuns.
        """
        db_session = SessionLocal()
        intentions = db_utils.get_most_common_intentions(db_session, user_id)
        db_session.close()
        return intentions

    def end_conversation(self, conversation_id: str):
        """
        Encerra uma conversa ativa.

        Args:
            conversation_id (str): Identificador da conversa.
        """
        db_session = SessionLocal()
        db_utils.end_conversation(db_session, conversation_id)
        db_session.close()

    def process_and_store_intentions(self, conversation_id: str):
        """
        Gera e armazena intenções com base nas mensagens da conversa.

        Args:
            conversation_id (str): Identificador da conversa.
        """
        db_session = SessionLocal()
        recommendations = self.model.get_intentions(db_session, conversation_id)
        db_utils.store_intentions(db_session, conversation_id, recommendations)
        print(f"Intenções processadas e armazenadas para a conversa {conversation_id}.")
        db_session.close()

    def handle_feedback(self, conversation_id: str, rating: int, comments: str):
        """
        Armazena o feedback de uma conversa.

        Args:
            conversation_id (str): Identificador da conversa.
            rating (int): Avaliação fornecida.
            comments (str): Comentários adicionais.
        """
        db_session = SessionLocal()
        feedback = Feedback(conversation_id=conversation_id, rating=rating, comments=comments)
        db_utils.store_feedback(db_session, feedback)
        db_session.close()

    def get_message(self, conversation_id: str, message_id: int):
        """
        Obtém uma mensagem específica em uma conversa.

        Args:
            conversation_id (str): Identificador da conversa.
            message_id (int): Identificador da mensagem.

        Returns:
            Message: Objeto de mensagem.
        """
        db_session = SessionLocal()
        message = db_utils.get_message(db_session, conversation_id, message_id)
        db_session.close()
        return message

    def get_attendant_status(self) -> bool:
        """
        Obtém o status atual do atendente (disponível ou indisponível).

        Returns:
            bool: True se o atendente estiver disponível, False caso contrário.
        """
        db_session = SessionLocal()
        status = db_utils.get_attendant_status(db_session)
        db_session.close()
        return status

    def analyze_sentiment(self, user_message: str) -> str:
        """
        Analisa o sentimento de uma mensagem do usuário.

        Args:
            user_message (str): Mensagem do usuário.

        Returns:
            str: Sentimento analisado.
        """
        return self.model.analyze_sentiment(user_message)

    def get_recommendations(self, user_id: str) -> list:
        """
        Obtém recomendações para um usuário específico.

        Args:
            user_id (str): Identificador do usuário.

        Returns:
            List[str]: Lista de recomendações.
        """
        db_session = SessionLocal()
        recommendations = self.model.get_recommendations(db_session, user_id)
        db_session.close()
        return recommendations

    def transcribe_summarize_and_store_image(self, conversation_id: str, image_path: str):
        """
        Transcreve, resume e armazena o conteúdo de uma imagem.

        Args:
            conversation_id (str): Identificador da conversa.
            image_path (str): Caminho da imagem.

        Returns:
            str: Resumo da imagem.
        """
        db_session = SessionLocal()
        response, transcription = self.model.transcribe_and_summarize_image(image_path)
        db_utils.store_file_summarization(db_session, conversation_id, 'image', transcription)
        db_session.close()
        return response

    def transcribe_summarize_and_store_audio(self, conversation_id: str, audio_path: str):
        """
        Transcreve, resume e armazena o conteúdo de um arquivo de áudio.

        Args:
            conversation_id (str): Identificador da conversa.
            audio_path (str): Caminho do arquivo de áudio.

        Returns:
            str: Resumo do áudio.
        """
        db_session = SessionLocal()
        response, transcription = self.model.transcribe_and_summarize_audio(audio_path)
        db_utils.store_file_summarization(db_session, conversation_id, 'audio', transcription)
        db_session.close()
        return response

    def save_temp_file(self, file: UploadFile) -> str:
        """
        Salva um arquivo temporariamente se for uma imagem válida.

        Args:
            file (UploadFile): Arquivo a ser salvo.

        Returns:
            str: Caminho do arquivo salvo.
        """
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        return temp_path

    def convert_pdf_to_image(self, file: UploadFile) -> str:
        """
        Converte um PDF para uma imagem (primeira página) e salva temporariamente.

        Args:
            file (UploadFile): Arquivo PDF a ser convertido.

        Returns:
            str: Caminho do arquivo de imagem salvo.
        
        Raises:
            HTTPException: Se não for possível converter o PDF em imagem.
        """
        temp_pdf_path = f"temp_{file.filename}"
        with open(temp_pdf_path, "wb") as f:
            f.write(file.file.read())

        images = convert_from_path(temp_pdf_path)
        if not images:
            os.remove(temp_pdf_path)
            raise HTTPException(status_code=400, detail="Could not convert PDF to image.")
        
        temp_image_path = f"temp_{os.path.splitext(file.filename)[0]}.png"
        images[0].save(temp_image_path, "PNG")
        os.remove(temp_pdf_path)
        
        return temp_image_path

    def convert_to_wav(self, file: UploadFile) -> str:
        """
        Converte um arquivo de áudio para o formato WAV e salva temporariamente.

        Args:
            file (UploadFile): Arquivo de áudio a ser convertido.

        Returns:
            str: Caminho do arquivo WAV salvo.

        Raises:
            HTTPException: Se não for possível converter o áudio para WAV.
        """
        temp_audio_path = f"temp_{file.filename}"
        with open(temp_audio_path, "wb") as f:
            f.write(file.file.read())

        try:
            audio = AudioSegment.from_file(temp_audio_path)
        except Exception as e:
            os.remove(temp_audio_path)
            raise HTTPException(status_code=400, detail=f"Could not convert audio to WAV: {str(e)}")

        temp_wav_path = f"temp_{os.path.splitext(file.filename)[0]}.wav"
        audio.export(temp_wav_path, format="wav")
        os.remove(temp_audio_path)

        return temp_wav_path
    
