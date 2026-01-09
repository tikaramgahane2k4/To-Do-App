// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const darkToggle = document.getElementById('darkToggle');
    
    // Check for saved dark mode preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkToggle.textContent = '☀️';
    }
    
    darkToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        darkToggle.textContent = isDark ? '☀️' : '🌙';
    });
});

// Submit Task Function
function submitTask(taskId) {
    fetch(`/submit/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✓ Task submitted successfully!");
            location.reload();
        } else {
            alert("✗ Error: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error submitting task!");
    });
}
