<template>
  <div class="skill-category">
    <div class="category-header">
      <div class="category-icon-wrapper">
        <!-- Icônes spécifiques et représentatives pour chaque catégorie -->
        <i v-if="title === 'Langages'" class="fas fa-code category-icon"></i>
        <i v-else-if="title === 'Frameworks'" class="fas fa-layer-group category-icon"></i>
        <i v-else-if="title === 'Outils'" class="fas fa-wrench category-icon"></i>
        <i v-else-if="title === 'Concepts'" class="fas fa-brain category-icon"></i>
        <i v-else-if="title === 'Niveau'" class="fas fa-award category-icon"></i>
        <i v-else :class="icon + ' category-icon'"></i>
      </div>
      <h4 class="category-title">{{ title }}</h4>
    </div>
    <div v-if="badgeLevel" class="level-badge" :class="'level-' + badgeLevel.toLowerCase()">
      {{ badgeLevel }}
    </div>
    <div v-else class="skills-list">
      <div v-for="(item, index) in items" :key="index" class="skill-item" :style="{'--i': index}">
        {{ item }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

type Props = {
  icon: string
  title: string
  items: string[]
  badgeLevel: string | null
}
const props = defineProps<Props>()
const { icon, title, items, badgeLevel } = props
</script>

<style scoped>
@import './src/styles/skills_category_style.css';
</style>