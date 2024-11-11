// ChatWidget.js

import React, { useState, useEffect, useRef } from 'react';
import { startConversation, sendMessage, endConversation, sendFeedback, uploadAudio, uploadImage } from '../services/api';
import './ChatWidget.css';
import icon1 from '../assets/icon1.png';
import icon2 from '../assets/icon2.png';
import icon3 from '../assets/icon3.png';
import icon4 from '../assets/icon4.png';
import icon5 from '../assets/icon5.svg';
import icon6 from '../assets/icon6.svg';
import icon7 from '../assets/icon7.svg';
import icon8 from '../assets/icon8.svg';
import icon9 from '../assets/icon9.png';
import icon10 from '../assets/icon10.svg';
import icon11 from '../assets/icon11.svg';
import icon12 from '../assets/icon12.svg';
import icon13 from '../assets/icon13.svg';
import icon14 from '../assets/icon14.png';


const ChatWidget = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [showNavbar, setShowNavbar] = useState(false);
    const [showPlaceholder, setShowPlaceholder] = useState(true);
    const [conversationId, setConversationId] = useState(null);
    const [messageId, setMessageId] = useState(null);
    const [intentions, setIntentions] = useState([]);
    const messagesEndRef = useRef(null);
    const inactivityTimeout = useRef(null);
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [recordingTime, setRecordingTime] = useState(0);
    const [isPaused, setIsPaused] = useState(false);
    const recordingInterval = useRef(null);
    const isRecordingCancelled = useRef(false);

    // Estados de Feedback
    const [isFeedback, setIsFeedback] = useState(false);
    const [feedbackStep, setFeedbackStep] = useState('rating'); // 'rating' ou 'comment'
    const [feedbackRating, setFeedbackRating] = useState(null);
    const [feedbackComments, setFeedbackComments] = useState('');

    // Flag para rastrear se o feedback já foi solicitado
    const [feedbackRequested, setFeedbackRequested] = useState(false);

    const formatTime = (timeInSeconds) => {
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = timeInSeconds % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    const handleSend = async () => {
        if (input.trim()) {
            if (isFeedback) {
                if (feedbackStep === 'rating') {
                    const rating = parseInt(input, 10);
                    if (rating >= 1 && rating <= 5) {
                        // Registrar a resposta do usuário como uma mensagem de feedback
                        const userRatingMessage = { text: `Nota: ${rating}`, sender: 'user', type: 'feedback' };
                        setMessages(prevMessages => [
                            ...prevMessages, 
                            userRatingMessage, // Adiciona a mensagem do usuário
                            { text: `Você deu uma nota ${rating}. Por favor, deixe um comentário:`, sender: 'bot', type: 'feedback' }
                        ]);

                        setFeedbackRating(rating);
                        setFeedbackStep('comment');
                        setInput(''); // Limpa o input após enviar
                    } else {
                        setMessages(prevMessages => [
                            ...prevMessages, 
                            { text: 'Por favor, insira um número válido entre 1 e 5.', sender: 'bot' }
                        ]);
                        return;
                    }
                } else if (feedbackStep === 'comment') {
                    // Registrar a resposta do usuário como uma mensagem de feedback
                    const userCommentMessage = { text: `Comentário: ${input}`, sender: 'user', type: 'feedback' };
                    setMessages(prevMessages => [
                        ...prevMessages, 
                        userCommentMessage // Adiciona a mensagem do usuário
                    ]);

                    setFeedbackComments(input);
                    setInput(''); // Limpa o input após enviar o comentário

                    // Enviar feedback para o backend
                    const feedbackData = {
                        id: 0,
                        conversation_id: conversationId,
                        rating: feedbackRating,
                        comments: input,
                        timestamp: new Date().toISOString()
                    };
                    try {
                        await sendFeedback(feedbackData);
                        // Enviar mensagem de agradecimento
                        setMessages(prevMessages => [
                            ...prevMessages, 
                            { text: 'Obrigado pelo seu feedback!', sender: 'bot', type: 'feedback' }
                        ]);

                        // Iniciar o timer de 30 segundos para resetar o chat
                        setTimeout(() => {
                            setMessages([]);
                            setIsFeedback(false);
                            setFeedbackStep('rating');
                            setFeedbackRating(null);
                            setFeedbackComments('');
                            setIsChatStarted(false);
                            setConversationId(null);
                            setFeedbackRequested(false); // Resetar a flag após enviar feedback
                        }, 30000); // 30 segundos de delay antes de resetar
                    } catch (error) {
                        setMessages(prevMessages => [
                            ...prevMessages, 
                            { text: 'Ocorreu um erro ao enviar seu feedback. Por favor, tente novamente mais tarde.', sender: 'bot' }
                        ]);
                    }
                }
            } else {
                // Fluxo normal de envio de mensagens
                const newMessages = [...messages, { text: input, sender: 'user' }];
                setMessages(newMessages);
                setInput('');

                try {
                    const response = await sendMessage(conversationId, input);
                    const botResponse = response.data.response;
                    setMessages([...newMessages, { text: botResponse, sender: 'bot' }]);
                } catch (error) {
                    console.error('Error sending message:', error);
                    setMessages([...newMessages, { text: 'Ocorreu um erro.', sender: 'bot' }]);
                }
            }
        }
    };

    // Função para tratar o clique nas intenções
    const handleIntentionClick = async (intention) => {
        if (intention.trim()) {
            // Adiciona a intenção como uma mensagem do usuário
            const newMessages = [...messages, { text: intention, sender: 'user' }];
            setMessages(newMessages);
            setInput(''); // Opcional: limpa o input

            try {
                const response = await sendMessage(conversationId, intention);
                const botResponse = response.data.response;
                setMessages([...newMessages, { text: botResponse, sender: 'bot' }]);
            } catch (error) {
                console.error('Erro ao enviar a intenção:', error);
                setMessages([...newMessages, { text: 'Ocorreu um erro ao processar sua solicitação.', sender: 'bot' }]);
            }
        }
    };

    const startRecording = async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // Mostrar uma caixa de diálogo de confirmação antes de acessar o microfone
            const permission = window.confirm("Este aplicativo deseja acessar o seu microfone para gravar áudio. Você permite?");
            if (!permission) {
                alert('Permissão para acessar o microfone foi negada.');
                return;
            }
    
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const recorder = new MediaRecorder(stream);
                const audioChunks = [];
    
                recorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
    
                // Adicione os eventos onpause e onresume aqui
                recorder.onpause = () => {
                    console.log('MediaRecorder paused');
                    setIsPaused(true);
                    clearInterval(recordingInterval.current); // Pausa o timer
                };
    
                recorder.onresume = () => {
                    console.log('MediaRecorder resumed');
                    setIsPaused(false);
                    recordingInterval.current = setInterval(() => {
                        setRecordingTime((prevTime) => prevTime + 1);
                    }, 1000); // Retoma o timer
                };
    
                recorder.onstop = async () => {
                    if (isRecordingCancelled.current) {
                        // Se a gravação foi cancelada, não faça nada
                        isRecordingCancelled.current = false;
                        return;
                    }
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const newMessages = [...messages, { audioUrl, sender: 'user', type: 'audio' }];
                    setMessages(newMessages);
    
                    // Enviar o áudio para o backend
                    try {
                        const response = await uploadAudio(conversationId, audioBlob);
                        const botResponse = response.data.response_message;
                        setMessages(prevMessages => [...prevMessages, { text: botResponse, sender: 'bot' }]);
                    } catch (error) {
                        console.error('Error uploading audio:', error);
                        setMessages(prevMessages => [...prevMessages, { text: 'Ocorreu um erro ao enviar o áudio.', sender: 'bot' }]);
                    }
                };
    
                recorder.start();
                setMediaRecorder(recorder);
                setIsRecording(true);
                setShowPlaceholder(false);
                setRecordingTime(0);
    
                resetInactivityTimeout();
    
                recordingInterval.current = setInterval(() => {
                    setRecordingTime((prevTime) => prevTime + 1);
                    resetInactivityTimeout();
                }, 1000);
            } catch (err) {
                console.error('Erro ao acessar o microfone:', err);
                alert('Não foi possível acessar o microfone. Por favor, verifique as permissões do navegador.');
            }
        } else {
            alert('Seu navegador não suporta gravação de áudio.');
        }
    };
    
    

    const cancelRecording = () => {
        if (mediaRecorder && (mediaRecorder.state === 'recording' || mediaRecorder.state === 'paused')) {
            isRecordingCancelled.current = true;
            mediaRecorder.stop();
            setIsRecording(false);
            setIsPaused(false);
            clearInterval(recordingInterval.current);
        }
    };

    const pauseRecording = () => {
        if (mediaRecorder) {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.pause();
            } else if (mediaRecorder.state === 'paused') {
                mediaRecorder.resume();
            }
        }
    }; 
    

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const newMessages = [...messages, { text: `Arquivo enviado: ${file.name}`, sender: 'user' }];
            setMessages(newMessages);
    
            try {
                const response = await uploadImage(conversationId, file);
                const botResponse = response.data.response_message;
                setMessages(prevMessages => [...prevMessages, { text: botResponse, sender: 'bot' }]);
            } catch (error) {
                console.error('Erro ao enviar a imagem:', error);
                setMessages(prevMessages => [...prevMessages, { text: 'Ocorreu um erro ao enviar a imagem.', sender: 'bot' }]);
            }
        }
    };
    

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const startChat = async () => {
        try {
            const userId = 'user1'; // Substitua com o ID do usuário apropriado
            const response = await startConversation(userId);
            setIsChatStarted(true);
            setFeedbackRequested(false); // Resetar a flag ao iniciar uma nova conversa
            // Armazena o ID da conversa no estado para usar ao enviar mensagens
            setConversationId(response.data.conversation_id);
            setIntentions(response.data.intentions); // Certifique-se que 'intentions' está vindo corretamente
            setMessages([]); // Limpa mensagens anteriores ao iniciar uma nova conversa
        } catch (error) {
            console.error('Error starting conversation:', error);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const formatBotResponse = (text) => {
        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br />');
        
        return formattedText;
    };

    const initiateFeedback = () => {
        if (!feedbackRequested) {
            console.log("Iniciando feedback");
            setFeedbackRequested(true);
            setIsFeedback(true);
            setFeedbackStep('rating');
            setMessages(prevMessages => [
                ...prevMessages, 
                { text: 'Por favor, avalie nossa conversa de 1 a 5:', sender: 'bot', type: 'feedback' }
            ]);
        }
    };

    const endConversationHandler = async () => {
        console.log("Chamando endConversationHandler");
        try {
            await endConversation(conversationId, ''); // Passe a mensagem de encerramento se necessário
            setMessages(prevMessages => [
                ...prevMessages, 
                { text: 'Conversa encerrada.', sender: 'bot' }
            ]);
            initiateFeedback(); // Iniciar o feedback após encerrar a conversa
        } catch (error) {
            console.error('Error ending conversation:', error);
            setMessages(prevMessages => [
                ...prevMessages, 
                { text: 'Ocorreu um erro ao encerrar a conversa.', sender: 'bot' }
            ]);
        }
    };

    const handleInactivityTimeout = async () => {
        if (conversationId) {
            if (!feedbackRequested) {
                await endConversationHandler();
            } else {
                // Apenas encerre a conversa sem solicitar feedback novamente
                try {
                    await endConversation(conversationId, '');
                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: 'Conversa encerrada devido à inatividade.', sender: 'bot' }
                    ]);
                    setIsChatStarted(false);
                    setIsFeedback(false);
                    setConversationId(null);
                    setFeedbackRequested(false); // Resetar a flag se necessário
                } catch (error) {
                    console.error('Error ending conversation:', error);
                    setMessages(prevMessages => [
                        ...prevMessages, 
                        { text: 'Ocorreu um erro ao encerrar a conversa.', sender: 'bot' }
                    ]);
                }
            }
        }
    };

    const resetInactivityTimeout = () => {
        if (inactivityTimeout.current) {
            clearTimeout(inactivityTimeout.current);
        }
        if (!isRecording){
            inactivityTimeout.current = setTimeout(handleInactivityTimeout, 60000); // 1 minuto (60000ms)
        } 
    };

    useEffect(() => {
        if (isOpen && (isChatStarted || isFeedback)) {
            scrollToBottom();
        }
    }, [messages, isOpen, isChatStarted, isFeedback]);

    const toggleNavbar = () => {
        setShowNavbar(!showNavbar);
    };

    useEffect(() => {
        return () => {
            if (mediaRecorder) {
                mediaRecorder.stop();
            }
        };
    }, [mediaRecorder]);

    useEffect(() => {
        if ((isChatStarted || isFeedback) && messages.length > 0) {
            resetInactivityTimeout();
        }

        return () => {
            if (inactivityTimeout.current) {
                clearTimeout(inactivityTimeout.current);
            }
        };
    }, [messages, isChatStarted, isFeedback]);

    return (
        <div className={`chat-container ${isOpen ? 'open' : ''}`}>
            <div className="chat-toggle" onClick={toggleChat}>
                {isOpen ? 'X' : (
                    <>
                        Dúvidas sobre remessas
                        <img src={icon1} alt="Ícone de dúvidas sobre remessas" className="chat-icon" />
                    </>
                )}
            </div>
            {isOpen && !isChatStarted && !isFeedback && (
                <div className="chat-start-screen">
                    <img src={icon2} alt="Ícone de IA" className="start-icon" />
                    <h2>Bem-vindo ao Talismã</h2>
                    <p>O chatbot da <img src={icon3} alt="Ícone da Brastell" className='' /></p>
                    <button className="start-button" onClick={startChat}>Iniciar Conversa</button>
                </div>
            )}
            {isOpen && (isChatStarted || isFeedback) && (
                <div className="chat-widget">
                    <div className="navbar-toggle">
                        <img />
                    </div>
                    {showNavbar && (
                        <div className="navbar">
                            <button className="close-navbar" onClick={toggleNavbar}>X</button>
                            <img src={icon2} alt="Ícone de IA" className="start-icon-navbar" />
                            <div className='name-navbar'>Talismã</div>
                            <img src={icon10} alt="Ícone de novo chat" className='novo-chat' onClick={startChat} />
                            <div className='novo-chat-text' onClick={startChat}>Novo Chat</div>
                            {/* Botão para encerrar conversa manualmente */}
                            <button className="end-conversation-button" onClick={endConversationHandler}>
                                Encerrar Conversa
                            </button>
                        </div>
                    )}
                    <div className="chat-messages">
                        {messages.length === 0 && (
                            <div className="chat-empty">
                                <img src={icon4} alt="Ícone de Dúvida" className="empty-icon" />
                                <p>Olá! Podemos iniciar nossa conversa com sugestões!</p>
                                <div className="suggestion-boxes">
                                    {intentions.slice(0, 3).map((intention, index) => (
                                        <div 
                                            key={index} 
                                            className="box" 
                                            onClick={() => handleIntentionClick(intention)}
                                        >
                                            {intention}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                        {messages.map((msg, index) => {
                            const isFeedbackMessage = msg.type === 'feedback';
                            const messageClasses = `chat-message ${msg.sender} ${isFeedbackMessage ? 'feedback' : ''}`;

                            console.log(`Mensagem ${index}:`, msg, "Classes:", messageClasses); // Debug

                            return (
                                <div key={index} className={messageClasses}>
                                    {msg.sender === 'bot' && (
                                        <>
                                            <img 
                                                src={icon2} 
                                                alt="Ícone de IA"
                                                className="bot-icon"
                                            />
                                            <div className="message-text-with-icon">
                                                <span dangerouslySetInnerHTML={{ __html: formatBotResponse(msg.text) }} />
                                                {!isFeedbackMessage && (
                                                    <>
                                                        <img 
                                                            src={icon5} 
                                                            alt="Ícone adicional"
                                                            className="icon5"
                                                        />
                                                        <div className="icon5-tooltip">Não gostei da resposta</div>
                                                    </>
                                                )}
                                            </div>
                                        </>
                                    )}
                                    {msg.sender === 'user' && (
                                        <div className="message-text">
                                            {msg.text}
                                            {msg.audioUrl && (
                                                <div className="audio-message">
                                                    <audio controls src={msg.audioUrl} />
                                                    {/* Removido o botão de excluir */}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className={`chat-input ${isRecording ? 'recording' : ''}`}>
                        {!isRecording && (
                            <div className="input-left">
                                <label htmlFor="file-upload" className="icon-left">
                                    <img src={icon7} alt="Ícone para upload de imagens" className="icon" />
                                    <div className="icon7-tooltip">Enviar Imagem</div>
                                    <input 
                                        type="file" 
                                        id="file-upload" 
                                        accept="image/*" 
                                        onChange={handleFileUpload} 
                                        style={{ display: 'none' }}
                                    />
                                </label>
                                <label htmlFor="audio-upload" className="icon-right">
                                    <img 
                                        src={icon8} 
                                        alt="Ícone para enviar áudio" 
                                        className="icon" 
                                        onClick={startRecording}
                                    />
                                    <div className="icon8-tooltip">Gravar áudio</div>
                                </label>
                            </div>
                        )}
                        <div className="input-container">
                            {isRecording ? (
                                <div className="recording-interface">
                                        <div className="controls-record">
                                            <div className="microphone-icon">🎤</div>
                                            <div className="recording-time">{formatTime(recordingTime)}</div>
                                            <div className={`audio-wave ${isPaused ? 'paused' : ''}`}> 
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                                <span className="wave-bar"></span>
                                            </div>
                                        </div>
                                    <div className="controls">
                                        {!isPaused ? (
                                            <img 
                                                src={icon11} 
                                                alt="Ícone para enviar áudio" 
                                                className="pause-recording fixed-icon icon" 
                                                onClick={pauseRecording}
                                            >
                                            </img>
                                        ) : (
                                            <img
                                                src={icon11} 
                                                alt="Ícone para enviar áudio" 
                                                className="pause-recording fixed-icon icon" 
                                                onClick={pauseRecording} 
                                        
                                            >
                                            </img>
                                        )}
                                        <img 
                                            className="send-recording fixed-icon" 
                                            src={icon13} 
                                            alt="Ícone para enviar gravação"
                                            onClick={() => {
                                                if (mediaRecorder) {
                                                    mediaRecorder.stop();
                                                    setIsRecording(false);
                                                    setIsPaused(false);
                                                    clearInterval(recordingInterval.current);
                                                }
                                            }}
                                        >
                                        </img>
                                        <img 
                                            className="cancel-recording fixed-icon" 
                                            src={icon14} 
                                            alt="Ícone para cancelar gravação"
                                            onClick={cancelRecording}
                                        ></img>
            
                                    </div>
        
                                </div>
                            ) : (
                                <input 
                                    type="text" 
                                    value={input} 
                                    onChange={(e) => setInput(e.target.value)} 
                                    placeholder={showPlaceholder ? "Digite uma mensagem..." : ""}
                                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                                />
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatWidget;
