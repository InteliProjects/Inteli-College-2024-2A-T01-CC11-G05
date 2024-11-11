import json
from typing import List
from .database_model import Conversation, Message
import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from ..utils.db_utils import get_disliked_messages
from PIL import Image
import pytesseract
import speech_recognition as sr
import typing_extensions as typing
import requests
import transformers
from transformers import pipeline

# Configuração da chave API do Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

class ChatbotModel:

    def __init__(self):
        # Inicializa o modelo generativo
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.model_img = pipeline("summarization", model="facebook/bart-large-cnn")
        self.url = "https://f527-34-126-191-118.ngrok-free.app/generate"
        

    def generate_response(self, messages: List[Message], user_input: str, sentiment: str) -> str:
        """
        Gera uma resposta baseada no histórico da conversa e no sentimento da última mensagem.

        Args:
            messages (List[Message]): Histórico das mensagens da conversa.
            user_input (str): Nova mensagem do usuário.
            sentiment (str): Sentimento da última mensagem do usuário.

        Returns:
            str: Resposta gerada pelo modelo.
        """
        conversation_history = "\n".join(
            [f"Usuário: {msg.user_message}\nBot: {msg.response_message}" for msg in messages]
        )

        prompt = (
            "Você é uma IA generativa que atua como atendente de remessas da Brastel Remit. "
            "Seu trabalho é responder as dúvidas dos clientes e solucionar problemas relacionados a remessas internacionais. "
            "Se for solicitar informações do usuário faça quebra de linha mais de uma vez para facilitar a leitura e adicione emojis para representar oque foi solicitado. "
            "Levando em consideração o sentimento da mensagem do usuário para formular a resposta. "
            "Aqui está o histórico da conversa:\n\n"
            f"{conversation_history}\n\n"
            "Sentimento da mensagem: "f"{sentiment}""\n"
            "Nova mensagem do Usuário: "f"{user_input}""\n"
            "Por favor, responda a esta mensagem:"
        )

        intention = self.get_intention(user_input)
        # Prepare o payload de teste
        payload = {
            "intent": intention,
            "question": user_input
        }

        # Cabeçalhos opcionais (se necessários)
        headers = {
            "Content-Type": "application/json"
        }

        try:
            # Envie a requisição POST
            response = requests.post(self.url, json=payload, headers=headers)

            # Verifique se a requisição foi bem-sucedida
            if response.status_code == 200:
                response_data = response.json()
                print("RESPOSTA GERADA: ", str(response_data.get('response', 'Sem resposta disponível')))
                return str(response_data.get('response', 'Sem resposta disponível'))
            else:
                return str(f"Erro na API: {response.status_code}, Resposta {response.text}")
        except Exception as e:
            # Captura qualquer exceção e exibe a mensagem de erro
            return f"Erro de conexão com a API: {str(e)}"

    def get_intention(self, message: str ) -> str:
        """
        Identifica a intenção presente na mensagem.

        Args:
            message (str): A mensagem do usuário.

        Returns:
            str: A intenção identificada.
        """
        prompt = (
            "Você é uma IA que identifica a intenção em mensagens dos usuários. "
            "As únicas intenções possíveis são: ['Saudação','Problemas/Duvidas sobre deposito', 'Tempo de Remessa','Pedido de envio via metodo ByPhone', 'Como se inscrever','Confirmacao de cambio/taxas','Problemas/Duvidas de atualizacao de dados cadastrais','Solicitacao de cartao de remessas', 'Cadastro de beneficiario','Acesso a conta', 'Termos e condicoes do servico','Problemas/Duvidas sobre remessas', 'Tempo de entrega do cartao','Reembolso', 'Cancelamento']."
            "Retorne apenas uma das intenções listadas que melhor corresponda à mensagem a seguir:\n\n"
            f"{message}"
        )

        response = self.model.generate_content(prompt).text.strip()
        return response

    def analyze_sentiment(self, user_message: str) -> str:
        """
        Analisa o sentimento de uma mensagem do usuário.

        Args:
            user_message (str): Mensagem do usuário a ser analisada.

        Returns:
            str: Sentimento da mensagem, que pode ser 'POSITIVE', 'NEGATIVE' ou 'NEUTRAL'.
        """
        prompt = (
            "Você é uma IA generativa que atua como atendente de remessas da Brastel Remit. "
            "Seu trabalho é analisar o sentimento das mensagens dos usuários e classificá-las como "
            "'POSITIVE' (positivo), 'NEGATIVE' (negativo) ou 'NEUTRAL' (neutro). "
            "Por favor, determine o sentimento da seguinte mensagem e retorne a classificação apropriada:\n\n"
            f"{user_message}"
        )
        
        response = self.model.generate_content(prompt).text
        sentiment = response.strip().upper()
        
        if sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
            return sentiment
        return "NEUTRAL"

    def get_intentions(self, db_session: Session, conversation_id: str) -> list:
        """
        Identifica as intenções presentes nas mensagens de uma conversa.

        Args:
            db_session (Session): Sessão do banco de dados.
            conversation_id (str): Identificador da conversa.

        Returns:
            list: Lista das intenções identificadas, limitadas aos tópicos esperados.
        """
        texts = [msg.user_message for msg in db_session.query(Message).filter_by(conversation_id=conversation_id).all()]

        if not texts:
            return []

        prompt = (
            "Você é uma IA generativa que atua como atendente de remessas da Brastel Remit. "
            "Seu trabalho é analisar as mensagens dos usuários e identificar todas as intenções presentes na conversa. "
            "As únicas intenções possíveis são: ['Problemas/Duvidas sobre deposito', 'Tempo de Remessa','Pedido de envio via metodo ByPhone', 'Como se inscrever','Confirmacao de cambio/taxas','Problemas/Duvidas de atualizacao de dados cadastrais','Solicitacao de cartao de remessas', 'Cadastro de beneficiario','Acesso a conta', 'Termos e condicoes do servico','Problemas/Duvidas sobre remessas', 'Tempo de entrega do cartao','Reembolso', 'Cancelamento']."
            "Retorne apenas a lista dos de todos os tópicos identificados na conversa, como segue:\n"
            "Seu retorno deve ser um list[str]"
            "Aqui estão as mensagens para análise:\n\n"
            f"{' '.join(texts)}"
        )


        response = self.model.generate_content(prompt, generation_config=genai.GenerationConfig(
        response_mime_type="application/json")).text

        response_list = eval(response)

        # Filtragem dos tópicos
        top_topics = [topic for topic in response_list if topic in ['Como depositar', 'Como fazer remessa', 'Tempo de remessa', 'Pedido de envio via metodo ByPhone', 'Como se inscrever', 'Confirmacao de cambio/taxas', 'Envio via Deposit Code', 'Registro/Atualizacao de Documento', 'Solicitacao de cartao de remessas', 'Cadastro de beneficiario', 'Acesso a conta', 'Termos e condicoes do servico', 'Problemas de remessa', 'Tempo de entrega do cartao', 'Reembolso', 'Regras do servico', 'Atualizacao de dados cadastrais', 'Cancelamento']][:3]

        return top_topics
    
    def check_consecutive_dislikes(self, db_session: Session, conversation_id: str) -> bool:
        """
        Verifica se há 3 dislikes consecutivos nas mensagens de uma conversa.

        Args:
            db_session (Session): Sessão do banco de dados.
            conversation_id (str): Identificador da conversa.

        Returns:
            bool: True se houver 3 dislikes consecutivos, False caso contrário.
        """
        disliked_messages = get_disliked_messages(db_session, conversation_id)
        consecutive_dislikes = 0

        for message in disliked_messages:
            consecutive_dislikes += 1
            if consecutive_dislikes == 3:
                return True
    
        return False

    def extract_text_with_pytesseract(self, image_path: str) -> str:
        """
        Extrai o texto de uma imagem usando o modelo Gemini AI.

        Args:
            image_path (str): Caminho para a imagem.

        Returns:
            str: Texto extraído da imagem.
        """
        image = Image.open(image_path)
        
        response = pytesseract.image_to_string(image, lang='por')

        return response

    def transcribe_and_summarize_image(self, image_path: str) -> str:
        """
        Transcreve o texto de uma imagem e fornece um resumo das informações principais.

        Args:
            image_path (str): Caminho para a imagem.

        Returns:
            tuple: Contém o resumo das informações principais e o texto transcrito da imagem.
        """
        transcribed_image = self.extract_text_with_pytesseract(image_path)

        response = self.model_img(transcribed_image)
        return response[0]['summary_text'], transcribed_image

    def transcribe_with_gemini(self, audio_path: str) -> str:
        """
        Transcreve o áudio usando o modelo Gemini AI.

        Args:
            audio_path (str): Caminho para o arquivo de áudio.

        Returns:
            str: Texto transcrito do áudio.
        """
        audio_file = genai.upload_file(path=audio_path)
        response = self.model.generate_content(["Transcreva o áudio", audio_file])
        return response.text

    def transcribe_and_summarize_audio(self, audio_path: str) -> str:
        """
        Transcreve o áudio e fornece um resumo das informações principais.

        Args:
            audio_path (str): Caminho para o arquivo de áudio.

        Returns:
            tuple: Contém o resumo das informações principais e o texto transcrito do áudio.
        """
        audio_file = genai.upload_file(path=audio_path)
        transcribed_audio = self.transcribe_with_gemini(audio_path)

        prompt = (
            "Você é uma IA generativa que atua como assistente de análise de áudio. "
            "Seu trabalho é analisar a transcrição de um áudio e fornecer um resumo das informações principais. "
            "Aqui está a transcrição do áudio:\n\n"
            f"{transcribed_audio}\n\n"
            "Por favor, forneça um resumo das informações principais contidas nesta transcrição."
        )

        response = self.model.generate_content(prompt).text
        return response, transcribed_audio
