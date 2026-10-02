// ================================================================
// MUKURU MONEY COACH
// AI chat
// ================================================================
//
// Render's free tier sleeps when idle, so the first request after a pause
// can take up to a minute while the server wakes. api-config.js widens the
// timeout and retries once, and the "thinking" bubble explains the wait
// rather than looking like a hang.

const userId = window.MUKURU_USER_ID;

// The demo signs in as a known user, so the coach greets them by name
// instead of asking who they are. See the static first message in
// index.html; the quick actions below attach to it on load.
let userName = window.MUKURU_USER_NAME;
let busy = false;

const chatForm = document.querySelector(".chat-input");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector(".chat-messages");


// ================================================================
// RENDERING
// ================================================================
// Uses textContent throughout, so coach replies can never inject HTML.


function scrollToLatest() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addUserMessage(message) {
    const el = document.createElement("div");
    el.textContent = message;
    el.classList.add("message", "user-message");
    chatMessages.appendChild(el);
    scrollToLatest();
}

function addCoachMessage(message) {
    const wrap = document.createElement("div");
    wrap.classList.add("message", "coach-message");

    const label = document.createElement("div");
    label.textContent = "Money Coach";
    label.classList.add("message-label");

    const content = document.createElement("div");
    content.textContent = message;
    content.classList.add("message-content");

    wrap.appendChild(label);
    wrap.appendChild(content);
    chatMessages.appendChild(wrap);
    scrollToLatest();
}

function addTyping() {
    const wrap = document.createElement("div");
    wrap.classList.add("message", "coach-message");

    const content = document.createElement("div");
    content.classList.add("message-content");
    content.textContent = "Money Coach is thinking... (the first reply can take up to a minute while the server wakes up)";

    wrap.appendChild(content);
    chatMessages.appendChild(wrap);
    scrollToLatest();
    return wrap;
}

function createSuggestionButtons(questions) {
    // Replace any previous row rather than stacking a new one each turn.
    document.querySelectorAll(".suggested-actions").forEach(function (node) {
        node.remove();
    });

    const box = document.createElement("div");
    box.classList.add("suggested-actions");

    questions.forEach(function (question) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = question;
        button.classList.add("suggestion-button");
        button.addEventListener("click", function () {
            messageInput.value = question;
            chatForm.requestSubmit();
        });
        box.appendChild(button);
    });

    chatMessages.appendChild(box);
    scrollToLatest();
}

function setBusy(value) {
    busy = value;
    messageInput.disabled = value;
    if (!value) {
        messageInput.focus();
    }
}


// ================================================================
// SEND
// ================================================================

// The greeting itself lives in index.html so it paints without waiting on
// this script; the quick actions are appended here once the DOM is ready.
window.addEventListener("DOMContentLoaded", function () {
    // Keep the static greeting in step with the configured user.
    document.querySelectorAll("[data-user-name]").forEach(function (node) {
        node.textContent = userName;
    });

    createSuggestionButtons([
        "Analyze my budget",
        "Check my goals",
        "What if I save R100 a week?",
        "Check my credit score"
    ]);
});

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    // The busy guard stops a double submit sending the message twice.
    if (message === "" || busy) {
        return;
    }

    addUserMessage(message);
    messageInput.value = "";
    setBusy(true);

    const typing = addTyping();

    window.mukuruFetch("/coach/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message: message })
    })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("HTTP " + response.status);
            }
            return response.json();
        })
        .then(function (data) {
            typing.remove();
            addCoachMessage(data.reply);

            if (data.suggested_actions && data.suggested_actions.length) {
                createSuggestionButtons(data.suggested_actions);
            }
        })
        .catch(function (error) {
            typing.remove();
            addCoachMessage(
                "Sorry " + userName +
                ", I couldn't reach the Money Coach right now. Please try again in a moment."
            );
            console.error("Chat error:", error);
        })
        .finally(function () {
            setBusy(false);
        });
});