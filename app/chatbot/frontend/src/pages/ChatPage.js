// frontend/src/pages/ChatPage.js
import React, { useState } from 'react';
import ChatInput from '../components/ChatInput';
import ChatOutput from '../components/ChatOutput';

const ChatPage = () => {
    const [messages, setMessages] = useState([]);

    const handleMessageSent = (response) => {
        setMessages([...messages, response]);
    };

    return (
        <div>
            <ChatInput onMessageSent={handleMessageSent} />
            {messages.map((message, index) => (
                <ChatOutput key={index} message={message} />
            ))}
        </div>
    );
};

export default ChatPage;
