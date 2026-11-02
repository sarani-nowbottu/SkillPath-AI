/**
 * mentor.js - SkillPath AI Mentor Conversational Client
 * Manages drawer open/close, message submission, quick action prompt pills, and real-time responses.
 */

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("mentor-drawer-toggle");
    const drawer = document.getElementById("mentor-drawer");
    const closeBtn = document.getElementById("mentor-drawer-close");
    const chatBody = document.getElementById("mentor-chat-body");
    const messageInput = document.getElementById("mentor-input-text");
    const sendBtn = document.getElementById("mentor-send-btn");
    const quickPills = document.querySelectorAll(".quick-pill");

    if (!drawer) return;

    // Toggle Drawer Open / Close
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            drawer.classList.add("open");
            if (messageInput) messageInput.focus();
            scrollToBottom();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            drawer.classList.remove("open");
        });
    }

    function scrollToBottom() {
        if (chatBody) {
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    // Append Message to UI
    function appendMessage(role, text) {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${role}`;
        
        // Simple Markdown / Newline conversion
        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
        
        bubble.innerHTML = formatted;
        chatBody.appendChild(bubble);
        scrollToBottom();
    }

    // Send Message Logic
    async function sendMessage(text) {
        const message = text || (messageInput ? messageInput.value.trim() : "");
        if (!message) return;

        appendMessage("user", message);
        if (messageInput) messageInput.value = "";

        // Typing indicator
        const typingEl = document.createElement("div");
        typingEl.className = "chat-bubble assistant";
        typingEl.id = "mentor-typing-indicator";
        typingEl.innerHTML = "<em>Thinking & analyzing your roadmap...</em>";
        chatBody.appendChild(typingEl);
        scrollToBottom();

        if (sendBtn) sendBtn.disabled = true;

        try {
            const resp = await fetch("/api/mentor/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });

            const data = await resp.json();
            
            // Remove typing indicator
            const indicator = document.getElementById("mentor-typing-indicator");
            if (indicator) indicator.remove();

            if (data.success && data.reply) {
                appendMessage("assistant", data.reply);
            } else {
                appendMessage("assistant", "Sorry, I encountered an issue processing that. Please try again.");
            }
        } catch (err) {
            console.error("Mentor chat error:", err);
            const indicator = document.getElementById("mentor-typing-indicator");
            if (indicator) indicator.remove();
            appendMessage("assistant", "Network connection error. Could not contact the career mentor.");
        } finally {
            if (sendBtn) sendBtn.disabled = false;
            if (messageInput) messageInput.focus();
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", () => sendMessage());
    }

    if (messageInput) {
        messageInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Quick prompt pills
    quickPills.forEach(pill => {
        pill.addEventListener("click", () => {
            const prompt = pill.getAttribute("data-prompt");
            if (prompt) {
                if (!drawer.classList.contains("open")) {
                    drawer.classList.add("open");
                }
                sendMessage(prompt);
            }
        });
    });
});
