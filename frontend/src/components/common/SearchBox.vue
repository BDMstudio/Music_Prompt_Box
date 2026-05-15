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
  <div class="relative w-full sm:w-auto min-w-0">
    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neon-magenta/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
    </svg>
    <input
      v-model="query"
      @input="onInput"
      type="text"
      placeholder="搜索风格、标签、描述..."
      class="w-full sm:w-64 border-b-2 border-neon-magenta bg-black/50 text-neon-cyan font-mono text-sm pl-10 pr-8 py-2
             placeholder:text-neon-magenta/65 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
    />
    <button
      v-if="query"
      @click="clear"
      class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-neon-magenta/50 hover:text-neon-magenta"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>
  </div>
</template>
