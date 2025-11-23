const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');
const sendBtn = document.getElementById('send-btn');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Adiciona mensagem do usuário
    addMessage(message, 'user');
    userInput.value = '';
    
    // Estado de loading
    setLoading(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error('Erro na comunicação com o servidor');

        const data = await response.json();
        
        // Adiciona resposta do bot
        addMessage(data.answer, 'bot');
        
        // Opcional: Mostrar contexto se desejar (console log por enquanto)
        console.log("Contexto usado:", data.context);

    } catch (error) {
        addMessage("Desculpe, ocorreu um erro ao processar sua solicitação.", 'bot');
        console.error(error);
    } finally {
        setLoading(false);
    }
});

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', `${sender}-message`);
    div.textContent = text;
    chatMessages.appendChild(div);
    scrollToBottom();
}

function setLoading(isLoading) {
    sendBtn.disabled = isLoading;
    if (isLoading) {
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.classList.add('message', 'bot-message');
        loadingDiv.textContent = 'Digitando...';
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
    } else {
        const loadingDiv = document.getElementById('loading-indicator');
        if (loadingDiv) loadingDiv.remove();
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
