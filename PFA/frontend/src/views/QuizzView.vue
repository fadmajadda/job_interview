<script setup>
import { ref, computed, nextTick } from 'vue'

import QuizzHeader from "@/components/quizz/QuizzHeader.vue"
import QuizzResult from "@/components/quizz/QuizzResult.vue"
import QuizzForm from "@/components/quizz/QuizzForm.vue"
import { generateQuizzQuestions } from "@/services/quizz_service.js"
import { validate_answer } from "@/services/answer_services.js"

// ===== STATE =====
const jobDescription = ref('')
const questionCount = ref(15)
const questionFormat = ref('qcm')
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const answerChecked = ref(false)
const isLoading = ref(false)
const error = ref(null)
const techData = ref(null)

// Open-ended question state
const userAnswer = ref('')
const isAnswerCorrect = ref(false)
const answerScore = ref(0)
const answerFeedback = ref('')
const isCheckingAnswer = ref(false)

// ===== COMPUTED PROPERTIES =====
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || null)
const progress = computed(() =>
  questions.value.length > 0
    ? Math.round((currentQuestionIndex.value + 1) / questions.value.length * 100)
    : 0
)
const isFirstQuestion = computed(() => currentQuestionIndex.value === 0)
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.value.length - 1)

// ===== METHODS =====

// Quiz Generation
async function generateQuestions() {
  if (!jobDescription.value.trim()) {
    error.value = "Veuillez entrer une offre d'emploi"
    return
  }
  if (questionCount.value < 5 || questionCount.value > 30) {
    error.value = "Veuillez entrer un nombre entre 5 et 30"
    return
  }

  isLoading.value = true
  error.value = null
  questions.value = []
  currentQuestionIndex.value = 0

  try {
    const response = await generateQuizzQuestions({
      job_description: jobDescription.value,
      question_count: questionCount.value,
      question_format: questionFormat.value
    })

    if (!response.data) {
      throw new Error('Aucune donnée reçue du serveur')
    }
    
    questions.value = questionFormat.value === 'qcm'
      ? randomizeCorrectAnswers(response.data.questions)
      : response.data.questions

    techData.value = response.data.tech_data
    resetQuestionState()
  } catch (err) {
    error.value = err.message || 'Une erreur est survenue'
    console.error('API Error:', err)
  } finally {
    isLoading.value = false
  }
}

// Answer Validation
// Answer Validation
async function validateAnswer() {
  if (!userAnswer.value.trim()) return;

  isCheckingAnswer.value = true;

  try {
    const response = await validate_answer({
      question: currentQuestion.value,
      user_answer: userAnswer.value
    });

    if (!response.data) {
      throw new Error('Erreur lors de la validation de la réponse');
    }

    isAnswerCorrect.value = response.data.is_correct;
    answerScore.value = response.data.score;
    answerFeedback.value = response.data.feedback || response.data.explanation;
    answerChecked.value = true;
  } catch (error) {
    console.error("Validation error:", error);
    isAnswerCorrect.value = false;
    answerFeedback.value = "Erreur lors de la validation";
    answerScore.value = 0;
  } finally {
    isCheckingAnswer.value = false;
  }
}

// Helper Functions
function randomizeCorrectAnswers(inputQuestions) {
  return inputQuestions.map(question => {
    const correctOption = question.options.find(opt => opt.correct)
    const incorrectOptions = question.options.filter(opt => !opt.correct)

    shuffleArray(incorrectOptions)

    const correctPosition = Math.floor(Math.random() * 5)
    const randomizedOptions = [
      ...incorrectOptions.slice(0, correctPosition),
      correctOption,
      ...incorrectOptions.slice(correctPosition)
    ]

    return {...question, options: randomizedOptions}
  })
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[array[i], array[j]] = [array[j], array[i]]
  }
  return array
}

// Quiz Navigation
function checkAnswer() {
  if (selectedOption.value !== null) {
    answerChecked.value = true
    scrollToExplanation()
  }
}

function nextQuestion() {
  if (!isLastQuestion.value) {
    currentQuestionIndex.value++
    resetQuestionState()
  }
}

function prevQuestion() {
  if (!isFirstQuestion.value) {
    currentQuestionIndex.value--
    resetQuestionState()
  }
}

function resetQuestionState() {
  selectedOption.value = null
  userAnswer.value = ''
  answerChecked.value = false
  isAnswerCorrect.value = false
  answerScore.value = 0
  answerFeedback.value = ''
  isCheckingAnswer.value = false
  scrollToTop()
}

function resetQuiz() {
  questions.value = []
  currentQuestionIndex.value = 0
  resetQuestionState()
}

// UI Helpers
function scrollToExplanation() {
  nextTick(() => {
    const explanation = document.querySelector('.explanation')
    if (explanation) {
      explanation.scrollIntoView({behavior: 'smooth'})
    }
  })
}

function showAnswer() {
  answerChecked.value = true
  scrollToExplanation()
}

function scrollToTop() {
  window.scrollTo({top: 0, behavior: 'smooth'})
}
</script>

<template>
  <div class="quiz-generator">
    <div class="quiz-container">
      <QuizzHeader />
      
      <main class="quiz-content">
        <QuizzForm
          v-model:description="jobDescription"
          v-model:count="questionCount"
          v-model:format="questionFormat"
          :isLoading="isLoading"
          :questions="questions"
          :techData="techData"
          @update:count="questionCount = $event"
          @update:format="questionFormat = $event"
          @generate="generateQuestions"
        />

        <QuizzResult
          :questions="questions"
          :currentIndex="currentQuestionIndex"
          :format="questionFormat"
          v-model:selected="selectedOption"
          :answerChecked="answerChecked"
          :isAnswerCorrect="isAnswerCorrect"
          :answerScore="answerScore"
          :answerFeedback="answerFeedback"
          v-model:userAnswer="userAnswer"
          :isCheckingAnswer="isCheckingAnswer"
          :progress="progress"
          :isFirst="isFirstQuestion"
          :isLast="isLastQuestion"
          @check-answer="checkAnswer"
          @validate-answer="validateAnswer"
          @prev-question="prevQuestion"
          @next-question="nextQuestion"
          @reset-quiz="resetQuiz"
        />

       
      </main>
    </div>
  </div>
</template>

<style scoped>
@import './src/styles/quizz_view_style.css';
</style>