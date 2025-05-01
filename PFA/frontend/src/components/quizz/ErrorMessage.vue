<script setup lang="ts">

defineProps<{
  error: string | null;  // Accept both string and null
}>()


const emits = defineEmits([
  'create',
  'submit'
])
</script>

<template>
  <div v-if="error" class="error"@click="emits('submit')">
    <i class="fas fa-exclamation-circle"></i> {{ error }}
  </div>
</template>

<style scoped>
/* Message d'erreur */
.error {
  color: var(--error-color);
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgba(244, 67, 54, 0.1);
  border-radius: 6px;
  border-left: 4px solid var(--error-color);
}
</style>