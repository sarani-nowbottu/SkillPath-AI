/**
 * app.js - SkillPath AI Client Interactions
 * Handles interactive checklists, live AJAX task toggling, and progress bar updates.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Task Checkbox Toggle Handler
    const taskCheckboxes = document.querySelectorAll(".task-checkbox");
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", async (e) => {
            const taskId = e.target.getAttribute("data-task-id");
            const taskItem = e.target.closest(".task-item");

            try {
                const response = await fetch(`/api/tasks/${taskId}/toggle`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                if (!response.ok) throw new Error("Network error toggling task");

                const data = await response.json();
                if (data.success) {
                    // Update visual state
                    if (data.is_completed) {
                        taskItem.classList.add("completed");
                    } else {
                        taskItem.classList.remove("completed");
                    }

                    // Update overall progress numbers and bar
                    const progressFill = document.getElementById("overall-progress-fill");
                    const progressText = document.getElementById("overall-progress-text");
                    const tasksCountText = document.getElementById("overall-tasks-count");

                    if (progressFill) {
                        progressFill.style.width = `${data.overall_progress}%`;
                    }
                    if (progressText) {
                        progressText.textContent = `${data.overall_progress}%`;
                    }
                    if (tasksCountText) {
                        tasksCountText.textContent = `${data.completed_tasks} / ${data.total_tasks} Tasks`;
                    }

                    // Check if stage is completed to update stage badge
                    const stageCard = taskItem.closest(".timeline-stage");
                    if (stageCard) {
                        const allTasksInStage = stageCard.querySelectorAll(".task-checkbox");
                        const completedInStage = stageCard.querySelectorAll(".task-checkbox:checked");
                        const stageBadge = stageCard.querySelector(".stage-status-badge");
                        if (allTasksInStage.length === completedInStage.length && allTasksInStage.length > 0) {
                            stageCard.classList.add("completed");
                            if (stageBadge) {
                                stageBadge.className = "badge badge-success stage-status-badge";
                                stageBadge.textContent = "Completed";
                            }
                        } else {
                            stageCard.classList.remove("completed");
                            if (stageBadge) {
                                stageBadge.className = "badge badge-primary stage-status-badge";
                                stageBadge.textContent = "In Progress";
                            }
                        }
                    }
                }
            } catch (err) {
                console.error("Failed to update task state:", err);
                e.target.checked = !e.target.checked; // Revert checkbox on error
                alert("Could not update task. Please check your internet connection.");
            }
        });
    });

    // 2. Reset Learning Path Confirmation
    const resetBtn = document.getElementById("reset-roadmap-btn");
    if (resetBtn) {
        resetBtn.addEventListener("click", async () => {
            if (confirm("Are you sure you want to reset your current learning roadmap and quiz attempts? Your student profile will be retained.")) {
                try {
                    const res = await fetch("/api/reset", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" }
                    });
                    const data = await res.json();
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    }
                } catch (e) {
                    alert("Error resetting roadmap: " + e.message);
                }
            }
        });
    }
});
