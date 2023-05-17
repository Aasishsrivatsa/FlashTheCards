// Handle form submission using JavaScript
function saveFlashcard(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    var form = document.getElementById('flashcardForm');
    var question = form.elements['question'].value;
    var answer = form.elements['answer'].value;
    var timeTaken = "0";
    var correctness = "True";

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_flashcard', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Flashcard saved!');
                    form.reset();
                } else {
                    alert('An error occurred while saving the flashcard.');
                }
            } else {
                alert('An error occurred while making the request.');
            }
        }
    };
    xhr.send(
        'question=' + encodeURIComponent(question) +
        '&answer=' + encodeURIComponent(answer) +
        '&time=' + encodeURIComponent(timeTaken) +
        '&correctness=' + encodeURIComponent(correctness)
    );
}

// Update card preview on question input change
document.getElementById('question').addEventListener('input', function() {
    var questionPreview = document.getElementById('questionPreview');
    questionPreview.textContent = this.value;
    updateCardHeight();
});

// Update card preview on answer input change
document.getElementById('answer').addEventListener('input', function() {
    var answerPreview = document.getElementById('answerPreview');
    answerPreview.textContent = this.value;
    updateCardHeight();
});

// Fix the issue where answer appears in place of the question
document.getElementById('answer').addEventListener('focus', function() {
    var questionPreview = document.getElementById('questionPreview');
    questionPreview.style.visibility = 'hidden';
});

document.getElementById('answer').addEventListener('blur', function() {
    var questionPreview = document.getElementById('questionPreview');
    questionPreview.style.visibility = 'visible';
});
