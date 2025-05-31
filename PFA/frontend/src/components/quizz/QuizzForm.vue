<script setup lang="ts">
import { ref, watch, defineEmits, defineProps } from 'vue'
import SkillCategory from './SkillCategory.vue'
import {QuestionFormatType} from "@/types/quizz-form.ts";
import { computed } from 'vue'

type TechData = {
  languages: string[]
  frameworks: string[]
  tools: string[]
  concepts: string[]
  level: string
}

const description = defineModel<string>('description',{default:''});
const count = defineModel<number>('count',{default:0});
const format = defineModel<QuestionFormatType>('format',{default:'qcm'});

const props = defineProps<{
  format: string
  isLoading: boolean
  techData: TechData | null
}>()

const emit = defineEmits<{
  (e: 'generate'): void
}>()

const categories = [
  { key: 'languages', icon: 'fas fa-code', title: 'Langages' },
  { key: 'frameworks', icon: 'fas fa-cubes', title: 'Frameworks' },
  { key: 'tools', icon: 'fas fa-tools', title: 'Outils' },
  { key: 'concepts', icon: 'fas fa-lightbulb', title: 'Concepts' },
  { key: 'level', icon: 'fas fa-chart-line', title: 'Niveau' }
]

// Erreurs locales
const errorDescription = computed(() => {
  return description.value.trim() === ''
    ? 'Veuillez entrer une offre d’emploi'
    : ''
})
const errorCount = computed(() => {
  return count.value < 2 || count.value > 30
    ? 'Le nombre de questions doit être entre 2 et 30'
    : ''
})

function onGenerate() {
  if (errorDescription.value || errorCount.value) return
  emit('generate')
}
</script>

<template>
  <section class="job-description-section">
    <h2><i class="fas fa-file-alt"></i> Offre d'emploi</h2>
    <div class="form-container">
      <textarea
        v-model="description"
        placeholder="Copiez ou collez le texte de l'offre d'emploi ici..."
        rows="10"
        class="description-textarea"
      ></textarea>
      <div v-if="errorDescription" class="error-message">{{ errorDescription }}</div>

      <div class="form-group">
        <label for="question-count">Nombre de questions à générer :</label>
        <input
          type="number"
          id="question-count"
          v-model.number="count"
          min="5"
          max="30"
          placeholder="Entre 5 et 30"
          class="form-input"
        >
        <p v-if="errorCount" class="error-message">{{ errorCount }}</p>
      </div>

      <div class="form-group">
        <label for="question-format">Format des questions :</label>
        <select
          id="question-format"
          v-model="format"
          class="format-selector form-input"
        >
          <option value="qcm">QCM (choix multiples)</option>
          <option value="qa">Questions/Réponses (ouvertes)</option>
        </select>
      </div>

      <div class="actions">
        <button @click="onGenerate" :disabled="isLoading" class="generate-button">
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? 'Génération en cours...' : 'Générer le quiz' }}
        </button>
      </div>
    </div>

    <div v-if="techData" class="skills-container">
      <h3 class="skills-title">Compétences clés détectées</h3>
      <div class="skills-grid">
        <skill-category
          v-for="cat in categories"
          :key="cat.key"
          :icon="cat.icon"
          :title="cat.title"
          :items="cat.key === 'level' ? [techData.level] : techData[cat.key]"
          :badge-level="cat.key === 'level' ? techData.level : null"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
@import './src/styles/quizz_form_style.css';
</style>