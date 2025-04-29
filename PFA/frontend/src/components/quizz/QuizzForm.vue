<script setup lang="ts">
import { ref, watch, defineEmits, defineProps } from 'vue'
import SkillCategory from './SkillCategory.vue'
import {QuestionFormatType} from "@/types/quizz-form.ts";


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

function onGenerate() {
  emit('generate')
}
</script>

<template>
  <section class="job-description-section    ">
    <h2><i class="fas fa-file-alt"></i> Offre d'emploi</h2>
    <textarea
      v-model="description"
      placeholder="Copiez ou collez le texte de l'offre d'emploi ici..."
      rows="10"
    ></textarea>

    <div class="form-group">
      <label for="question-count">Nombre de questions à générer :</label>
      <input
        type="number"
        id="question-count"
        v-model.number="count"
        min="5"
        max="30"
        placeholder="Entre 5 et 30"
      >
    </div>

    <div class="form-group">
      <label for="question-format">Format des questions :</label>
      <select
        id="question-format"
        v-model="format"
        class="format-selector"
      >
        <option value="qcm">QCM (choix multiples)</option>
        <option value="qa">Questions/Réponses (ouvertes)</option>
      </select>
    </div>

    <div class="actions">
      <button @click="onGenerate" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        {{ isLoading ? 'Génération en cours...' : 'Générer le quiz' }}
      </button>
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
.job-description-section {
  flex: 1;
  position: sticky;
  top: 20px;
  margin: 10px;
  overflow-x: hidden;
  height: calc(100vh - 100px);
  overflow-y: auto;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}


.job-description-section h2 {
  font-size: 1.5rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.job-description-section textarea {
  width: 100%;
  min-height: 300px;

  border: 2px solid var(--border-color);
  border-radius: 6px;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.job-description-section textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.job-description-section .form-group {
  margin: 1rem 0;
}

.job-description-section .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.job-description-section .form-group input[type="number"],
.job-description-section .form-group .format-selector {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.job-description-section .form-group input[type="number"]:focus,
.job-description-section .form-group .format-selector:focus {
  outline: none;
  border-color: var(--primary-color);
}

.job-description-section .actions {
  margin: 1rem 0;
}

.job-description-section .actions button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
}

.job-description-section .actions button:disabled {
  background-color: var(--disabled-color);
  cursor: not-allowed;
}

.job-description-section .loading-spinner {
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

@keyframes spin { to { transform: rotate(360deg); } }

.job-description-section .skills-container {
  margin-top: 2.5rem;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #eaeaea;
}

.job-description-section .skills-title {
  color: #2c3e50;
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-color);
  display: inline-block;
}

.job-description-section .skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Scoped styles for SkillCategory are defined in its component */

/* Responsive adjustments */
@media (max-width: 768px) {
  .job-description-section {
    position: static;
    height: auto;
    max-height: none;
  }
}
</style>
