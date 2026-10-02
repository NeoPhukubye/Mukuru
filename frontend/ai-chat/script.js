const userId = "grace";

let userName = "";
let waitingForName = true;

const chatForm = document.querySelector(".chat-input");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector(".chat-messages");


/* ================================================================
   SEND MESSAGE
   ================================================================ */

chatForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }


    /* ============================================================
       GET USER'S NAME
       ============================================================ */

    if (waitingForName) {

        userName = message;

        waitingForName = false;

        addUserMessage(userName);

        addCoachMessage(
            `Nice to meet you, ${userName}! 👋 How can I help you with your money today?`
        );

        createSuggestionButtons();

        messageInput.value = "";

        return;
    }


    /* ============================================================
       NORMAL MONEY COACH MESSAGE
       ============================================================ */

    addUserMessage(message);

    messageInput.value = "";


    /* ============================================================
       SEND MESSAGE TO BACKEND
       ============================================================ */

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

    .then(response => {

        if (!response.ok) {
            throw new Error("API request failed");
        }

        return response.json();
    })

    .then(data => {

        addCoachMessage(
            `${userName}, ${data.reply}`
        );

        chatMessages.scrollTop = chatMessages.scrollHeight;
    })

    .catch(error => {

        addCoachMessage(
            `Sorry ${userName}, I couldn't connect to the Money Coach right now.`
        );

        console.error("Error:", error);
    });
});


/* ================================================================
   ADD USER MESSAGE
   ================================================================ */

function addUserMessage(message) {

    const userMessage = document.createElement("div");

    userMessage.textContent = message;

    userMessage.classList.add(
        "message",
        "user-message"
    );

    chatMessages.appendChild(userMessage);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


/* ================================================================
   ADD COACH MESSAGE
   ================================================================ */

function addCoachMessage(message) {

    const coachMessage = document.createElement("div");

    coachMessage.classList.add(
        "message",
        "coach-message"
    );


    const label = document.createElement("div");

    label.textContent = "Money Coach";

    label.classList.add("message-label");


    const content = document.createElement("div");

    content.textContent = message;

    content.classList.add("message-content");


    coachMessage.appendChild(label);
    coachMessage.appendChild(content);

    chatMessages.appendChild(coachMessage);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


/* ================================================================
   SUGGESTION BUTTONS
   ================================================================ */

function createSuggestionButtons() {

    const suggestedActions = document.createElement("div");

    suggestedActions.classList.add(
        "suggested-actions"
    );


    const questions = [
        "Analyze my budget",
        "Check my goals",
        "Simulate savings",
        "Check my credit score"
    ];


    questions.forEach(function(question) {

        const button = document.createElement("button");

        button.type = "button";

        button.textContent = question;

        button.classList.add(
            "suggestion-button"
        );


        button.addEventListener("click", function() {

            messageInput.value = question;

            chatForm.requestSubmit();
        });


        suggestedActions.appendChild(button);
    });


    chatMessages.appendChild(suggestedActions);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

