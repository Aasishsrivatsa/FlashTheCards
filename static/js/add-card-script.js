// Handle form submission using JavaScript
function saveFlashcard(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    var form = document.getElementById('flashcardForm');
    var question = form.elements['question'].value;
    var answer = form.elements['answer'].value;
    var xhr = new XMLHttpRequest();
    
    xhr.open('POST', '/save_flashcard', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    showError(response);
                    form.reset();
                }
                else {
                    showError(response)
                }
            }
            else {
                alert('Error making the request')
            }
        }
    };
    xhr.send('question=' + encodeURIComponent(question) +
        '&answer=' + encodeURIComponent(answer));
}

function showError(response) {
    var messageElement = document.getElementById('message');
    messageElement.textContent = response.message;
    messageElement.style.color = response.success ? 'green' : 'red';

    setTimeout(function() {
        messageElement.textContent = '';
            }, 3000);
}
