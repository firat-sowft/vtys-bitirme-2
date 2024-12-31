function toggleArticles(button) {
    const publications = button.nextElementSibling;
    if (publications.style.display === 'none' || publications.style.display === '') {
        publications.style.display = 'block';
        button.textContent = 'Makaleleri Gizle';
    } else {
        publications.style.display = 'none';
        button.textContent = 'Makaleleri Göster';
    }
}

function toggleCommentSection(button) {
    const commentSection = button.parentElement.querySelector('.comment-section');
    if (commentSection.style.display === 'none' || commentSection.style.display === '') {
        commentSection.style.display = 'block';
    } else {
        commentSection.style.display = 'none';
    }
}

function toggleLike(button, akademisyen, makale) {
    const isLiked = button.classList.contains('liked');
    fetch('/toggle_like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            akademisyen: akademisyen,
            makale: makale,
            liked: !isLiked,
            user_name: 'Misafir Kullanıcı'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likeCountSpan = button.nextElementSibling;
            let likeCount = parseInt(likeCountSpan.textContent);
            if (isLiked) {
                button.classList.remove('liked');
                button.textContent = '♡';
                likeCount = Math.max(0, likeCount - 1); // Ensure like count does not go below 0
            } else {
                button.classList.add('liked');
                button.textContent = '❤️';
                likeCount++;
            }
            likeCountSpan.textContent = likeCount;
        }
    });
}

function submitComment(button, akademisyen, makale) {
    const commentSection = button.parentElement;
    const textarea = commentSection.querySelector('textarea');
    const comment = textarea.value.trim();

    if (comment) {
        fetch('/submit_comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                akademisyen: akademisyen,
                makale: makale,
                comment: comment,
                user_name: 'Misafir Kullanıcı'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const commentsList = commentSection.querySelector('.comments-list');
                const newComment = document.createElement('div');
                newComment.classList.add('comment');
                newComment.innerHTML = `
                    <img src="/static/profile.png" alt="Profil Simgesi" class="comment-profile-image">
                    <div class="comment-content">
                        <p><strong>Misafir Kullanıcı</strong></p>
                        <p>${comment}</p>
                    </div>
                `;
                commentsList.appendChild(newComment);
                textarea.value = '';

                // Update comment count
                const commentCountSpan = button.parentElement.previousElementSibling.querySelector('.comment-count');
                let commentCount = parseInt(commentCountSpan.textContent);
                commentCount++;
                commentCountSpan.textContent = commentCount;
            }
        });
    }
}