<template>
  <section v-if="questions.length > 0" class="question-section">
    <h2>
      <i class="fas fa-question-circle"></i>
      Question {{ currentIndex + 1 }}/{{ questions.length }}
    </h2>

    <div class="progress-container">
      <div class="progress-bar">
        <div class="progress" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="progress-text">{{ Math.round(progress) }}% complété</div>
    </div>

    <article class="question-card">
      <h3>{{ questions[currentIndex].question }}</h3>

      <div v-if="format === 'qcm'" class="qcm-container">
        <form @submit.prevent="emitCheckAnswer">
          <fieldset>
            <legend class="sr-only">Options de réponse</legend>
            <div
              v-for="(option, idx) in questions[currentIndex].options"
              :key="idx"
              class="option"
              :class="{
                'option-selected': localSelected === idx && !answerChecked,
                'option-correct': answerChecked && option.correct,
                'option-incorrect': answerChecked && !option.correct && localSelected === idx
              }"
              @click="updateSelected(idx)"
            >
              <input
                type="radio"
                :id="`option${idx}`"
                :value="idx"
                v-model="localSelected"
                :disabled="answerChecked"
              >
              <label :for="`option${idx}`">
                {{ option.text }}
              </label>
              <i v-if="answerChecked && option.correct" class="fas fa-check-circle option-icon correct-icon"></i>
              <i v-if="answerChecked && !option.correct && localSelected === idx" class="fas fa-times-circle option-icon incorrect-icon"></i>
            </div>
          </fieldset>

          <div class="form-actions">
            <button
              v-if="!answerChecked"
              type="submit"
              :disabled="localSelected === null"
              class="primary"
            >
              <i class="fas fa-check"></i> Valider la réponse
            </button>
          </div>
        </form>
      </div>
      <div v-else class="qa-container">
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
          <div v-if="isAnswerCorrect" class="feedback-header correct-feedback">
            <i class="fas fa-check-circle"></i>
            <span>Réponse correcte ({{ Math.round(answerScore * 100) }}%)</span>
          </div>
          <div v-else class="feedback-header incorrect-feedback">
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

          <button @click="emitResetQuiz" type="button" class="secondary reset-button">
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
  if (!props.answerChecked) {
    localSelected.value = idx
  }
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
@import './src/styles/quizz_result_style.css';
</style>