<script setup>
import {ref, computed, watch} from 'vue'
import ErrorMessage from "@/components/quizz/ErrorMessage.vue";
import QuizzHeader from "@/components/quizz/QuizzHeader.vue";
import QuizzResult from "@/components/quizz/QuizzResult.vue";
import QuizzForm from "@/components/quizz/QuizzForm.vue";
import {generateQuizzQuestions} from "@/services/quizz_service.js";

// State
const jobDescription = ref('');
const questionCount = ref(15)
const questionFormat = ref('qcm')
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const answerChecked = ref(false)
const isLoading = ref(false)
const error = ref(null)
const techData = ref(null)

const userAnswer = ref('')
const isAnswerCorrect = ref(false)
const answerScore = ref(0)
const answerFeedback = ref('')
const isCheckingAnswer = ref(false)

// Computed
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || null)
const progress = computed(() =>
    questions.value.length > 0
        ? Math.round((currentQuestionIndex.value + 1) / questions.value.length * 100)
        : 0
)
const isFirstQuestion = computed(() => currentQuestionIndex.value === 0)
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.value.length - 1)

// Methods
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

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      new Error(errorData.message || 'Erreur lors de la génération des questions')
    }

    const data = await response.json()
    questions.value = questionFormat.value === 'qcm'
        ? randomizeCorrectAnswers(data.questions)
        : data.questions

    techData.value = data.tech_data
    resetQuestionState()
  } catch (err) {
    error.value = err.message || 'Une erreur est survenue'
    console.error('API Error:', err)
  } finally {
    isLoading.value = false
  }
}

async function validateAnswer() {
  if (!userAnswer.value.trim()) return

  isCheckingAnswer.value = true

  try {
    const response = await fetch('http://localhost:5000/validate_answer', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        question: currentQuestion.value,
        user_answer: userAnswer.value
      })
    })

    if (!response.ok)  new Error('Erreur lors de la validation')

    const result = await response.json()
    isAnswerCorrect.value = result.is_correct
    answerScore.value = result.score
    answerFeedback.value = result.feedback || result.explanation
    answerChecked.value = true
  } catch (error) {
    console.error("Validation error:", error)
    isAnswerCorrect.value = false
    answerFeedback.value = "Erreur lors de la validation"
    answerScore.value = 0
  } finally {
    isCheckingAnswer.value = false
  }
}

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
  <div class="main-container ">
    <div class="container">
      <QuizzHeader/>
      <main>
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

        <ErrorMessage :error="error"/>
      </main>
    </div>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.main-container {
  max-width: 1380px;
  margin: 0 auto;

}

/* Conteneur principal */
.container {
  width: 100%;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}


/* Layout principal */
main {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  width: 100%;
  margin-top: 2rem;
}


.navigation-buttons button {
  flex: 1;
  min-width: 120px;
}







</style>