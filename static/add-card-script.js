// Handle form submission using JavaScript
function saveFlashcard(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    var form = document.getElementById('flashcardForm');
    var question = form.elements['question'].value;
    var answer = form.elements['answer'].value;
    var timeTaken = "0";
    var correctness = "True";


    // Create a new AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_flashcard', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Flashcard saved!');
                    // Clear the form inputs
                    form.reset();
                } else {
                    alert('An error occurred while saving the flashcard.');
                }
            } else {
                alert('An error occurred while making the request.');
            }
        }
    };
    // Send the request with the form data
    xhr.send('question=' + encodeURIComponent(question) +
                '&answer=' + encodeURIComponent(answer) +
                '&time=' + encodeURIComponent(timeTaken) +
                '&correctness=' + encodeURIComponent(correctness));
}

// Add event listener to handle form submission
document.getElementById('flashcardForm').addEventListener('submit', saveFlashcard);
