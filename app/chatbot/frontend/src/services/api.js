const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;


export const startConversation = async (userId) => {
    try {
        const response = await fetch(`${BACKEND_URL}/start_conversation/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error starting conversation:', error);
        throw error;
    }
};

export const sendMessage = async (conversationId, userMessage) => {
    try {
        const response = await fetch(`${BACKEND_URL}/send_message/${conversationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_message: userMessage }),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};

export const endConversation = async (conversationId, userMessage) => {
    try {
        const response = await fetch(`${BACKEND_URL}/end_conversation/${conversationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_message: userMessage }),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error ending conversation:', error);
        throw error;
    }
};


export const sendFeedback = async (feedbackData) => {
    try {
        const response = await fetch(`${BACKEND_URL}/user_feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(feedbackData),
        });
        if (!response.ok) {
            throw new Error('Erro ao enviar feedback');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending feedback:', error);
        throw error;
    }
};


export const uploadAudio = async (conversationId, audioBlob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav'); // 'file' deve corresponder ao nome do parâmetro no backend

    try {
        const response = await fetch(`${BACKEND_URL}/upload_audio/${conversationId}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Erro ao enviar o áudio.');
        }

        const data = await response.json();
        return data; // Retorna o objeto JSON completo
    } catch (error) {
        console.error('Erro ao fazer upload do áudio:', error);
        throw error;
    }
};

export const uploadImage = async (conversationId, file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${BACKEND_URL}/upload_image/${conversationId}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Erro ao enviar a imagem.');
        }

        const data = await response.json();
        return data; // Retorna o objeto JSON completo
    } catch (error) {
        console.error('Erro ao fazer upload da imagem:', error);
        throw error;
    }
};

