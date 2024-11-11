from datetime import datetime
from http.client import HTTPException
from typing import List
import uuid
from ..models.database_model import (
    Conversation, Message, Feedback, AttendantStatus, User, FileSummarization, FileTypeEnum
)
from sqlalchemy.orm import Session, joinedload
import yaml
from collections import Counter

def start_new_conversation(db_session: Session) -> str:
    """
    Inicia uma nova conversa e retorna o identificador da conversa.
    
    Args:
        db_session (Session): Sessão do banco de dados.
    
    Returns:
        str: Identificador da nova conversa.
    """
    new_conversation = Conversation(id=str(uuid.uuid4()))
    db_session.add(new_conversation)
    db_session.commit()
    return new_conversation.id

def store_message(db_session: Session, conversation_id: str, user_message: str, response_message: str):
    """
    Armazena uma mensagem em uma conversa específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
        user_message (str): Mensagem do usuário.
        response_message (str): Mensagem de resposta do chatbot.
    """
    conversation = db_session.query(Conversation).filter_by(id=conversation_id).first()
    message = Message(
        conversation_id=conversation_id,
        user_message=user_message,
        response_message=response_message
    )
    conversation.messages.append(message)
    db_session.add(message)
    db_session.commit()

def record_dislike(db_session: Session, message_id: int, conversation_id: str):
    """
    Registra um desagrado para uma mensagem específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        message_id (int): Identificador da mensagem.
        conversation_id (str): Identificador da conversa.
    """
    message = get_message(db_session, conversation_id, message_id)
    if message:
        message.disliked = True
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Message not found.")

def get_message(db_session: Session, conversation_id: str, message_id: int) -> Message:
    """
    Obtém uma mensagem específica de uma conversa.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
        message_id (int): Identificador da mensagem.
    
    Returns:
        Message: Mensagem encontrada.
    """
    return db_session.query(Message).filter_by(id=message_id, conversation_id=conversation_id).first()

def get_disliked_messages(db_session: Session, conversation_id: str) -> List[Message]:
    """
    Obtém todas as mensagens desagradas de uma conversa específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
    
    Returns:
        List[Message]: Lista de mensagens desagradas.
    """
    return (
        db_session.query(Message)
        .filter(Message.conversation_id == conversation_id, Message.disliked.is_(True))
        .order_by(Message.timestamp)
        .all()
    )

def get_messages_for_conversation(db_session: Session, conversation_id: str) -> List[Message]:
    """
    Obtém todas as mensagens de uma conversa específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
    
    Returns:
        List[Message]: Lista de mensagens da conversa.
    """
    return db_session.query(Message).filter_by(conversation_id=conversation_id).all()

def get_all_conversations(db_session: Session, user_id: str) -> List[Conversation]:
    """
    Obtém todas as conversas de um usuário específico.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        user_id (str): Identificador do usuário.
    
    Returns:
        List[Conversation]: Lista de conversas do usuário.
    """
    return db_session.query(Conversation).filter_by(user_id=user_id).all()

def get_conversation_history(db_session: Session, conversation_id: str):
    """
    Obtém o histórico de uma conversa específica, incluindo mensagens e sumarizações de arquivos.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
    
    Returns:
        Conversation: Objeto da conversa com o histórico.
    """
    return db_session.query(Conversation).options(
        joinedload(Conversation.messages),
        joinedload(Conversation.file_summarizations)
    ).filter_by(id=conversation_id).first()

def store_intentions(db_session: Session, conversation_id: str, recommendations: List[str]):
    """
    Armazena as intenções em uma conversa específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
        recommendations (List[str]): Lista de intenções.
    """
    conversation = db_session.query(Conversation).filter_by(id=conversation_id).first()
    if conversation:
        conversation.intentions = recommendations
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Conversation not found.")

def end_conversation(db_session: Session, conversation_id: str):
    """
    Encerra uma conversa, definindo o status como 'ended' e o tempo de término.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
    """
    conversation = db_session.query(Conversation).filter_by(id=conversation_id).first()
    if conversation:
        conversation.status = "ended"
        conversation.end_time = datetime.utcnow()
        db_session.commit()
    else:
        raise HTTPException(status_code=404, detail="Conversation not found.")

def store_feedback(db_session: Session, feedback: Feedback):
    """
    Armazena o feedback fornecido.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        feedback (Feedback): Objeto de feedback.
    """
    db_session.add(feedback)
    db_session.commit()

def get_attendant_status(db_session: Session) -> str:
    """
    Obtém o status atual do atendente.
    
    Args:
        db_session (Session): Sessão do banco de dados.
    
    Returns:
        str: Status do atendente.
    """
    status = db_session.query(AttendantStatus).order_by(AttendantStatus.updated_at.desc()).first()
    return status.status if status else None

def reset_id_sequence(session: Session, table_name: str, column_name: str):
    """
    Reseta a sequência de IDs para uma tabela específica.
    
    Args:
        session (Session): Sessão do banco de dados.
        table_name (str): Nome da tabela.
        column_name (str): Nome da coluna de ID.
    """
    if session.bind.dialect.name == 'postgresql':
        session.execute(f"""
            SELECT setval(pg_get_serial_sequence('{table_name}', '{column_name}'), 
            coalesce(max({column_name}), 1) + 1, false) FROM {table_name};
        """)
        session.commit()

def load_mock_data(session: Session):
    """
    Carrega dados mockados para o banco de dados a partir de um arquivo YAML.
    
    Args:
        session (Session): Sessão do banco de dados.
    """
    with open("app/database/config/database_mock.yaml", "r") as file:
        data = yaml.safe_load(file)

    # Verificar se há usuários no banco de dados
    user_count = session.query(User).count()
    if user_count == 0:
        for user_data in data['users']:
            user = User(**user_data)
            session.add(user)
        session.commit()
    else:
        print("Usuários já existem no banco de dados. Ignorando carga de dados mocados para usuários.")

    # Verificar se há conversas no banco de dados
    conversation_count = session.query(Conversation).count()
    if conversation_count == 0:
        for conversation_data in data['conversations']:
            user_id = conversation_data.pop('user_id', None)
            messages_data = conversation_data.pop('messages', [])
            
            conversation = Conversation(**conversation_data)
            if user_id:
                conversation.user_id = user_id
            session.add(conversation)
            
            for message_data in messages_data:
                message = Message(conversation_id=conversation.id, **message_data)
                session.add(message)
        session.commit()
    else:
        print("Conversas já existem no banco de dados. Ignorando carga de dados mocados para conversas.")

    # Verificar se há feedbacks no banco de dados
    feedback_count = session.query(Feedback).count()
    if feedback_count == 0:
        for feedback_data in data['feedbacks']:
            feedback = Feedback(**feedback_data)
            session.add(feedback)
        session.commit()
    else:
        print("Feedbacks já existem no banco de dados. Ignorando carga de dados mocados para feedbacks.")

    # Verificar se há status do atendente no banco de dados
    attendant_status_count = session.query(AttendantStatus).count()
    if attendant_status_count == 0:
        for attendant_data in data['attendant_status']:
            attendant = AttendantStatus(**attendant_data)
            session.add(attendant)
        session.commit()
    else:
        print("Status do atendente já existem no banco de dados. Ignorando carga de dados mocados para status do atendente.")
    
    reset_id_sequence(session, 'messages', 'id')
    reset_id_sequence(session, 'feedbacks', 'id')

def get_most_common_intentions(db_session: Session, user_id: str) -> List[str]:
    """
    Obtém as intenções mais comuns de um usuário específico.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        user_id (str): Identificador do usuário.
    
    Returns:
        List[str]: Lista das intenções mais comuns.
    """
    conversations = get_all_conversations(db_session, user_id)
    all_intentions = []

    for conversation in conversations:
        if conversation.intentions:
            all_intentions.extend(conversation.intentions)

    intention_counter = Counter(all_intentions)
    return [intention for intention, count in intention_counter.most_common(3)]

def store_file_summarization(db_session: Session, conversation_id: str, file_type: str, summarization_text: str):
    """
    Armazena a sumarização de um arquivo associado a uma conversa.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
        file_type (str): Tipo do arquivo (audio, image).
        summarization_text (str): Texto da sumarização.
    """
    file_summarization = FileSummarization(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        file_type=FileTypeEnum[file_type.upper()],
        summarization=summarization_text
    )
    db_session.add(file_summarization)
    db_session.commit()

def get_last_message(db_session: Session, conversation_id: str) -> Message:
    """
    Obtém a última mensagem de uma conversa específica.
    
    Args:
        db_session (Session): Sessão do banco de dados.
        conversation_id (str): Identificador da conversa.
    
    Returns:
        Message: Última mensagem da conversa.
    """
    return db_session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.timestamp.desc()).first()
