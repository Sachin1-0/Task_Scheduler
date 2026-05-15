document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        const themeIcon = themeToggleBtn.querySelector('i');
        const themeText = document.getElementById('theme-text');
        const htmlElement = document.documentElement;

        // Update icon based on current theme
        if (htmlElement.getAttribute('data-bs-theme') === 'dark') {
            themeIcon.classList.replace('fa-moon', 'fa-sun');
            if (themeText) themeText.textContent = 'Light Mode';
        }

        themeToggleBtn.addEventListener('click', function() {
            // Need to make an AJAX request to save user preference
            fetch('/toggle_theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (data.dark_mode) {
                        htmlElement.setAttribute('data-bs-theme', 'dark');
                        themeIcon.classList.replace('fa-moon', 'fa-sun');
                        if (themeText) themeText.textContent = 'Light Mode';
                    } else {
                        htmlElement.setAttribute('data-bs-theme', 'light');
                        themeIcon.classList.replace('fa-sun', 'fa-moon');
                        if (themeText) themeText.textContent = 'Dark Mode';
                    }
                }
            });
        });
    }

    // Add polling for push notifications
    function checkOverdueTasks() {
        fetch('/api/tasks/pending')
            .then(response => {
                if(!response.ok) throw new Error("Not logged in or error");
                return response.json();
            })
            .then(data => {
                const now = new Date();
                const notifiedTasks = JSON.parse(localStorage.getItem('notifiedTasks') || '[]');

                data.tasks.forEach(task => {
                    if (task.due_date && task.due_time) {
                        const taskDateTime = new Date(`${task.due_date}T${task.due_time}`);
                        // If task is overdue and we haven't notified yet
                        if (now >= taskDateTime && !notifiedTasks.includes(task.id)) {
                            if (Notification.permission === 'granted') {
                                new Notification('Task Deadline Reached', {
                                    body: `Complete your task now: ${task.title}`
                                });
                                notifiedTasks.push(task.id);
                                localStorage.setItem('notifiedTasks', JSON.stringify(notifiedTasks));
                            }
                        }
                    }
                });
            })
            .catch(err => console.log('Polling tasks error:', err));
    }

    // Request permission and start polling
    if ("Notification" in window) {
        if (Notification.permission !== "granted" && Notification.permission !== "denied") {
            Notification.requestPermission();
        }
        // Check every 60 seconds
        setInterval(checkOverdueTasks, 60000);
        // Check immediately on load
        checkOverdueTasks();
    }
});
