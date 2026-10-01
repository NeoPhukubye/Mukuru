const chatForm = document.querySelector(".chat-input");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector(".chat-messages");
chatForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const message = messageInput.value;
    console.log(message);
    const userMessage = document.createElement("div");
    userMessage.textContent = message;
    userMessage.classList.add("message", "user-message");
    chatMessages.appendChild(userMessage);
    
});