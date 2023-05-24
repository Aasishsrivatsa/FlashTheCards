

function getFlashcard() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/flashcard', true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          updateFlashcard(response);
        } else {
          alert('Error fetching the flashcard');
        }
      }
    };
    xhr.send();
  }
  
  function updateFlashcard(flashcard) {
    var titleElement = document.querySelector('.card-question');
    var descriptionElement = document.querySelector('.card-answer');
  
    // Replace pipes with commas in the question and answer
    var question = flashcard.question.replace(/\|/g, ',');
    var answer = flashcard.answer.replace(/\|/g, ',');
  
    titleElement.textContent = question;
    descriptionElement.textContent = answer;
  }
  

   