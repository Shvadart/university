let currentUser = '';

window.onload = function () {
  // For demonstration purposes, you can pre-populate some comments
  setUserName();
  loadCommentsFromFile();
};

function addComment() {
  const authorInput = document.getElementById('authorInput');
  const commentInput = document.getElementById('commentInput');

  const author = authorInput.value.trim();
  const comment = commentInput.value.trim();

  if (author !== '' && comment !== '') {
    displayComment({ author, comment });

    // Clear the input fields
    
    commentInput.value = '';
  }
}

function saveCommentsToServer(comments) {
  fetch('http://127.0.0.1:3000/saveComments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ comments }),
  })
    .then(response => {
      if (response.ok) {
        alert('Комментарии успешно сохранены!');
      } else {
        alert('Не удалось сохранить комментарии.');
      }
    })
    .catch(error => {
      console.error('Error saving comments:', error);
      alert('Failed to save comments.');
    });
}

function loadCommentsFromServer() {
  fetch('http://127.0.0.1:3000/loadComments')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to load comments.');
      }
      return response.json();
    })
    .then(comments => {
      comments.forEach(comment => displayComment(comment));
    })
    .catch(error => {
      console.error('Error loading comments:', error);
      displaySampleComments(); // Display sample comments if the file doesn't exist
    });
}

function saveCommentsToFile() {
  const comments = Array.from(document.querySelectorAll('#comments div')).map(
    commentDiv => {
      const author = commentDiv.dataset.author;
      const comment = commentDiv.dataset.comment;
      return { author, comment };
    }
  );

  saveCommentsToServer(comments);
}

function loadCommentsFromFile() {
  loadCommentsFromServer();
}


function downloadToFile(content, filename, contentType) {
  const blob = new Blob([content], { type: contentType });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);

  // Update the download path to the 'public' folder
  a.download = `${filename}`;
  a.click();
}

function setUserName() {
  currentUser = prompt('Пожалуйста введите имя пользователя:');
  if (currentUser) {
    document.getElementById('authorInput').value = currentUser;
    document.getElementById('authorInput').disabled = true;
  }
}

function editComment(commentDiv) {
  const author = commentDiv.dataset.author;

  if (author === currentUser) {
    const commentText = commentDiv.dataset.comment;
    const newComment = prompt('Отредактируйте комментарий:', commentText);

    if (newComment !== null) {
      commentDiv.dataset.comment = newComment;
      commentDiv.querySelector('strong').innerText = `${author}:`;
      commentDiv.querySelector('span').innerText = newComment;
    }
  } else {
    alert('Вы можете редактировать только свои комментарии.');
  }
}

function deleteComment(commentDiv) {
  const author = commentDiv.dataset.author;

  if (author === currentUser) {
    commentDiv.remove();
  } else {
    alert('Вы можете удалять только свои комментарии!');
  }
}

function displayComment({ author, comment }) {
  const commentsDiv = document.getElementById('comments');
  const commentDiv = document.createElement('div');
  commentDiv.dataset.author = author;
  commentDiv.dataset.comment = comment;
  commentDiv.innerHTML = `
        <strong>${author}:</strong> <span>${comment}</span>
        <button onclick="editComment(this.parentNode)">Редактировать</button>
        <button onclick="deleteComment(this.parentNode)">Удалить</button>
    `;
  commentsDiv.appendChild(commentDiv);
}
