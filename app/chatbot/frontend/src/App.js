// frontend/src/App.js
import React from 'react';
import ChatWidget from './components/ChatWidget';


const App = () => {
    return (
            <div>
                <div style={{ width: '100%', height: '100vh', border: 'none' }}>
                <iframe
                    src="https://brastelremit.jp/por/home"
                    title="BrastelRemit"
                    style={{ width: '100%', height: '100%', border: 'none' }}
                ></iframe>
            </div>
            <ChatWidget />
        </div>
    );
};

export default App;


