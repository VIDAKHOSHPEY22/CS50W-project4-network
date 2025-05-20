document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.onclick = function() {
            const postId = this.dataset.postId;
            fetch(`/like/${postId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if ('likes_count' in data) {
                    this.querySelector('.like-count').textContent = data.likes_count;
                    this.classList.toggle('btn-outline-primary', !data.liked);
                    this.classList.toggle('btn-primary', data.liked);
                    this.textContent = (data.liked ? "Unlike" : "Like") + ` (${data.likes_count})`;
                }
            });
        };
    });
});

// Helper to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken'; // مقدار درست برای نام کوکی CSRF
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
