<template>
  <section v-if="questions.length > 0" class="question-section">
    <h2>
      <i class="fas fa-question-circle"></i>
      Question {{ currentIndex + 1 }}/{{ questions.length }}
    </h2>

    <div class="progress-bar">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>

    <article class="question-card">
      <h3>{{ questions[currentIndex].question }}</h3>

      <div v-if="format === 'qcm'">
        <form @submit.prevent="emitCheckAnswer">
          <fieldset>
            <legend class="sr-only">Options de réponse</legend>
            <div
              v-for="(option, idx) in questions[currentIndex].options"
              :key="idx"
              class="option"
              @click="updateSelected(idx)"
            >
              <input
                type="radio"
                :id="`option${idx}`"
                :value="idx"
                v-model="localSelected"
                :disabled="answerChecked"
              >
              <label
                :for="`option${idx}`"
                :class="{
                  correct: answerChecked && option.correct,
                  incorrect: answerChecked && !option.correct && localSelected === idx
                }"
              >
                {{ option.text }}
              </label>
            </div>
          </fieldset>

          <div class="form-actions">
            <button
              v-if="!answerChecked"
              type="submit"
              :disabled="localSelected === null"
              class="primary"
            >
              Valider la réponse
            </button>
          </div>
        </form>
      </div>
      <div v-else>
        <div v-if="!answerChecked" class="answer-input-section">
          <textarea
            v-model="localUserAnswer"
            placeholder="Saisissez votre réponse ici..."
            rows="4"
            class="answer-input"
          ></textarea>
          <button
            @click="emitValidateAnswer"
            class="primary"
            :disabled="!localUserAnswer.trim() || isCheckingAnswer"
          >
            <span v-if="isCheckingAnswer" class="loading-spinner"></span>
            {{ isCheckingAnswer ? 'Validation en cours...' : 'Valider ma réponse' }}
          </button>
        </div>
        <div v-if="answerChecked" class="feedback">
          <div v-if="isAnswerCorrect" class="correct-feedback">
            <i class="fas fa-check-circle"></i>
            <span>Réponse correcte ({{ Math.round(answerScore * 100) }}%)</span>
          </div>
          <div v-else class="incorrect-feedback">
            <i class="fas fa-times-circle"></i>
            <span>Réponse partiellement correcte ({{ Math.round(answerScore * 100) }}%)</span>
          </div>

          <div class="feedback-explanation">
            <p>{{ answerFeedback }}</p>
          </div>

          <div class="expected-answer">
            <h4>Réponse optimale :</h4>
            <p>{{ questions[currentIndex].answer }}</p>
          </div>
        </div>
      </div>

      <div v-if="answerChecked" class="explanation">
        <p><strong>Explication :</strong> {{ questions[currentIndex].explication }}</p>
        <div class="navigation-buttons">
          <button
            @click="emitPrevQuestion"
            type="button"
            class="secondary"
            :disabled="isFirst"
          >
            <i class="fas fa-arrow-left"></i> Précédente
          </button>

          <button
            @click="emitNextQuestion"
            type="button"
            class="primary"
            :disabled="isLast"
          >
            Suivante <i class="fas fa-arrow-right"></i>
          </button>

          <button @click="emitResetQuiz" type="button" class="secondary">
            <i class="fas fa-redo"></i> Nouveau quiz
          </button>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import {QuestionFormatType} from "@/types/quizz-form.js";

type Option = { text: string; correct: boolean }

type Question = {
  question: string
  options: Option[]
  answer: string
  explication: string
}

const props = defineProps<{
  questions: Question[]
  currentIndex: number
  format: QuestionFormatType;
  selected: number | null
  answerChecked: boolean
  isAnswerCorrect: boolean
  answerScore: number
  answerFeedback: string
  userAnswer: string
  isCheckingAnswer: boolean
  progress: number
  isFirst: boolean
  isLast: boolean
}>()

const emit = defineEmits<{
  (e: 'update:selected', val: number | null): void
  (e: 'update:userAnswer', val: string): void
  (e: 'check-answer'): void
  (e: 'validate-answer'): void
  (e: 'prev-question'): void
  (e: 'next-question'): void
  (e: 'reset-quiz'): void
}>()

// Local v-models
const localSelected = ref<number | null>(props.selected)
const localUserAnswer = ref<string>(props.userAnswer)

watch(() => props.selected, v => (localSelected.value = v))
watch(localSelected, v => emit('update:selected', v))

watch(() => props.userAnswer, v => (localUserAnswer.value = v))
watch(localUserAnswer, v => emit('update:userAnswer', v))

function updateSelected(idx: number) {
  localSelected.value = idx
}

function emitCheckAnswer() {
  emit('check-answer')
}

function emitValidateAnswer() {
  emit('validate-answer')
}

function emitPrevQuestion() {
  emit('prev-question')
}

function emitNextQuestion() {
  emit('next-question')
}

function emitResetQuiz() {
  emit('reset-quiz')
}
</script>

<style scoped>


/* Titres */
h1, h2, h3, h4 {
  color: var(--text-color);
  margin-bottom: 1rem;
}

h1 {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
}

h2 {
  font-size: 1.5rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
}

h3 {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

/* Question section styles */
.question-section {
  flex: 1;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.question-section h2 {
  font-size: 1.5rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--progress-bg);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

.question-card {
  background: var(--background-light);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.option {
  margin: 0.75rem 0;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  transition: all 0.2s;
  cursor: pointer;
}

.option:hover {
  background: #f0f0f0;
  border-color: var(--primary-color);
}

.option input[type="radio"] {
  margin-right: 0.75rem;
  cursor: pointer;
}

.correct {
  color: var(--success-color);
  font-weight: bold;
  background-color: rgba(76, 175, 80, 0.1);
}

.incorrect {
  color: var(--error-color);
  text-decoration: line-through;
  background-color: rgba(244, 67, 54, 0.1);
}

.answer-input-section {
  margin: 1.5rem 0;
}

.answer-input {
  width: 100%;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 6px;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
}

.answer-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.feedback-explanation {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  margin: 1rem 0;
}

.correct-feedback {
  color: var(--success-color);
  font-weight: bold;
}

.incorrect-feedback {
  color: var(--error-color);
  font-weight: bold;
}

.expected-answer {
  background-color: #e8f5e9;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.explanation {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--info-bg);
  border-radius: 6px;
  border-left: 4px solid var(--success-color);
}

.navigation-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: space-between;
}

.navigation-buttons button {
  flex: 1;
  min-width: 120px;
}

.navigation-buttons button.secondary {
  background-color: white;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.navigation-buttons button.secondary:hover:not(:disabled) {
  background-color: #f0f0f0;
}
</style>
