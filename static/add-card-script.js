// Handle form submission using JavaScript
function saveFlashcard() {
    var form = document.getElementById('flashcardForm');
    var question = form.elements['question'].value;
    var answer = form.elements['answer'].value;

    // Replace commas with pipes
    question = question.replace(/,/g, '|');
    answer = answer.replace(/,/g, '|');

    // Create a new AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_flashcard', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // Flashcard saved successfully
                    alert('Flashcard saved!');
                    // Clear the form inputs
                    form.reset();
                } else {
                    // Error occurred while saving flashcard
                    alert('An error occurred while saving the flashcard.');
                }
            } else {
                // Error occurred while making the request
                alert('An error occurred while making the request.');
            }
        }
    };
    // Send the request with the form data
    xhr.send('question=' + encodeURIComponent(question) +
                '&answer=' + encodeURIComponent(answer));
}
