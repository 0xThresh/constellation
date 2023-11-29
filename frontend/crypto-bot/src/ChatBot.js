import AWS from 'aws-sdk';
import React, { useState } from 'react';

const ChatBot = () => {
    const [inputText, setInputText] = useState('');
    const [messages, setMessages] = useState([]);

    AWS.config.update({
        region: process.env.REACT_APP_AWS_REGION,
        credentials: new AWS.Credentials({
            accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
            secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
        }),
    });

    const client = new AWS.LexRuntimeV2();

    const sendMessageToBot = async (message) => {
        const params = {
            botId: process.env.REACT_APP_BOT_ID,
            botAliasId: process.env.REACT_APP_BOT_ALIAS_ID,
            localeId: 'en_US', // Specify the locale, if your bot supports multiple locales
            sessionId: 'test-user-session', // Use a session identifier for the user
            text: message,
        };

        try {
            const response = await client.recognizeText(params).promise();
            setMessages([...messages, { from: 'bot', text: response.messages[0].content }]);
        } catch (err) {
            console.error('Error sending message to bot:', err);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        setMessages([...messages, { from: 'user', text: inputText }]);
        sendMessageToBot(inputText);
        setInputText('');
    };

    return (
        <div>
            <h2>Chat with our Bot</h2>
            <div>
                {messages.map((message, index) => (
                    <p key={index}><b>{message.from}:</b> {message.text}</p>
                ))}
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ChatBot;
