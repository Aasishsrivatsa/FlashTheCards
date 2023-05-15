const flashcardElement = document.getElementById('flashcard');
const flipButton = document.getElementById('flip-btn');
const nextButton = document.getElementById('next-btn');
const questionElement = document.getElementById('question');
const answerElement = document.getElementById('answer');

const flashcards = [
  { question: 'What is the capital of France?', answer: 'Paris' },
  { question: 'Who painted the Mona Lisa?', answer: 'Leonardo da Vinci' },
  // Add more flashcards here
];

let currentFlashcardIndex = 0;
let isFlipped = false;

function showFlashcard(index) {
  const flashcard = flashcards[index];
  questionElement.textContent = flashcard.question;
  answerElement.textContent = flashcard.answer;
}

function flipFlashcard() {
  flashcardElement.classList.toggle('flipped');
  isFlipped = !isFlipped;
}

function nextFlashcard() {
  currentFlashcardIndex = (currentFlashcardIndex + 1) % flashcards.length;
  showFlashcard(currentFlashcardIndex);
  flashcardElement.classList.remove('flipped');
  isFlipped = false;
}

flipButton.addEventListener('click', flipFlashcard);
nextButton.addEventListener('click', nextFlashcard);

// Show the first flashcard initially
showFlashcard(currentFlashcardIndex);
