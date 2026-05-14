<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  search: [query: string]
}>()

const query = ref('')
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function onInput() {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = setTimeout(() => {
    emit('search', query.value)
  }, 300)
}

function clear() {
  query.value = ''
  emit('search', '')
}
</script>

<template>
  <div class="relative">
    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-sub dark:text-dark-text-sub" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
    </svg>
    <input
      v-model="query"
      @input="onInput"
      type="text"
      placeholder="搜索风格、标签、描述..."
      class="w-64 pl-10 pr-8 py-2 bg-white dark:bg-dark-surface border-2 border-foreground dark:border-dark-border text-sm text-foreground dark:text-dark-text-main font-medium
             placeholder:text-text-sub dark:placeholder:text-dark-text-sub focus:outline-none focus:border-primary-red transition-colors duration-200"
    />
    <button
      v-if="query"
      @click="clear"
      class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-text-sub dark:text-dark-text-sub hover:text-foreground dark:hover:text-dark-text-main"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>
  </div>
</template>
