const userId = "grace";
let userName = "";

const chatForm = document.querySelector(".chat-input");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector(".chat-messages");


chatForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    // Get the user's name on their first message
    if (userName === "") {
        userName = message;

        const userMessage = document.createElement("div");
        userMessage.textContent = message;
        userMessage.classList.add("message", "user-message");
        chatMessages.appendChild(userMessage);

        const coachMessage = document.createElement("div");
        coachMessage.textContent =
            `Nice to meet you, ${userName}! 👋 I'm here to help you manage your money and reach your goals. You can ask me anything, or choose one of the options below to get started.`;
        coachMessage.classList.add("message", "coach-message");
        chatMessages.appendChild(coachMessage);

        createSuggestionButtons();

        messageInput.value = "";

        return;
    }


    // Display the user's message
    const userMessage = document.createElement("div");

    userMessage.textContent = message;

    userMessage.classList.add("message", "user-message");

    chatMessages.appendChild(userMessage);

    messageInput.value = "";


    // Send the message to the backend
    fetch("https://mukuru-jb1l.onrender.com/coach/chat", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            user_id: userId,
            message: message
        })
    })

    .then(response => response.json())

    .then(data => {
        const coachMessage = document.createElement("div");

        coachMessage.textContent = `${userName}, ${data.reply}`;

        coachMessage.classList.add("message", "coach-message");

        chatMessages.appendChild(coachMessage);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    })

    .catch(error => {
        const coachMessage = document.createElement("div");

        coachMessage.textContent =
            `Sorry ${userName}, I couldn't connect to the Money Coach right now.`;

        coachMessage.classList.add("message", "coach-message");

        chatMessages.appendChild(coachMessage);

        console.error("Error:", error);
    });
});


// Create the suggested question buttons
function createSuggestionButtons() {
    const suggestedActions = document.createElement("div");

    suggestedActions.classList.add("suggested-actions");

    const questions = [
        "Analyze my budget",
        "Check my goals",
        "Simulate savings",
        "Check my credit score"
    ];

    questions.forEach(question => {
        const button = document.createElement("button");

        button.type = "button";

        button.textContent = question;

        button.classList.add("suggestion-button");

        button.addEventListener("click", function() {
            messageInput.value = question;

            chatForm.dispatchEvent(new Event("submit"));
        });

        suggestedActions.appendChild(button);
    });

    chatMessages.appendChild(suggestedActions);
}