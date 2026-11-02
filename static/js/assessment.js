/**
 * assessment.js - SkillPath AI Diagnostic Quiz Engine
 * Tracks selected options, validates full completion, submits to backend, and handles result presentation.
 */

document.addEventListener("DOMContentLoaded", () => {
    const quizForm = document.getElementById("diagnostic-quiz-form");
    if (!quizForm) return;

    // Highlight selected options visually
    const optionLabels = document.querySelectorAll(".quiz-option");
    optionLabels.forEach(label => {
        const radio = label.querySelector("input[type='radio']");
        radio.addEventListener("change", () => {
            const questionName = radio.getAttribute("name");
            document.querySelectorAll(`input[name="${questionName}"]`).forEach(r => {
                r.closest(".quiz-option").classList.remove("selected");
            });
            if (radio.checked) {
                label.classList.add("selected");
            }
        });
    });

    // Handle Form Submission via AJAX
    quizForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(quizForm);
        const answers = {};
        for (let [key, val] of formData.entries()) {
            if (key.startsWith("q_")) {
                const qId = key.replace("q_", "");
                answers[qId] = parseInt(val, 10);
            }
        }

        const totalQuestions = parseInt(quizForm.getAttribute("data-total-questions"), 10);
        const answeredCount = Object.keys(answers).length;

        if (answeredCount < totalQuestions) {
            if (!confirm(`You have answered ${answeredCount} of ${totalQuestions} questions. Do you want to submit anyway? (Unanswered questions will count as incorrect).`)) {
                return;
            }
        }

        const submitBtn = document.getElementById("submit-quiz-btn");
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = "Analyzing Skill Profile...";
        }

        try {
            const response = await fetch("/api/assessment/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: json.stringify ? JSON.stringify({ answers }) : "{}"
            });

            if (!response.ok) throw new Error("Server error submitting quiz.");

            const result = await response.json();
            if (result.success && result.redirect_url) {
                window.location.href = result.redirect_url;
            }
        } catch (err) {
            console.error("Quiz submission failure:", err);
            alert("Error submitting assessment: " + err.message);
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = "Submit Diagnostic Assessment";
            }
        }
    });
});
