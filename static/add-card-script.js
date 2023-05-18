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
                    alert('Flashcard saved!');
                    form.reset();
                }
                else {
                    alert('An error occurred while saving the flashcard.');
                }
            }
            else {
                alert('An error occurred while making the request.');
            }
        }
    };
    xhr.send('question=' + encodeURIComponent(question) +
        '&answer=' + encodeURIComponent(answer));
}