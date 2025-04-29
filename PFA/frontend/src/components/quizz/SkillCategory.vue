<template>
  <div class="skill-category">
    <div class="category-header">
      <i :class="icon + ' category-icon'"></i>
      <h4 class="category-title">{{ title }}</h4>
    </div>
    <div v-if="badgeLevel" class="level-badge" :class="'level-' + badgeLevel">
      {{ badgeLevel }}
    </div>
    <div v-else class="skills-list">
      <div v-for="(item, index) in items" :key="index" class="skill-item">
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
.skill-category {
  background: #f8fafc;
  border-radius: 10px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.category-icon {
  color: var(--primary-color);
  font-size: 1.2rem;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.skill-item {
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #4a5568;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.skill-item:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.level-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: capitalize;
  margin-top: 0.5rem;
}

.level-junior {
  background: #f0f9ff;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.level-mid {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.level-senior {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}
</style>
