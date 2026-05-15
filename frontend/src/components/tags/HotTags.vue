<script setup lang="ts">
import { computed } from 'vue'
import { useTagsStore } from '@/stores/tags'
import { useStylesStore } from '@/stores/styles'

const tagsStore = useTagsStore()
const stylesStore = useStylesStore()

const activeTag = computed(() => {
  const q = stylesStore.searchQuery.trim().toLowerCase()
  return q || null
})

function toggleTag(tag: string) {
  if (activeTag.value === tag.toLowerCase()) {
    // deselect — clear search
    stylesStore.setSearch('')
  } else {
    stylesStore.setSearch(tag)
  }
  stylesStore.loadStyles()
}
</script>

<template>
  <div v-if="tagsStore.hotTags.length > 0" class="flex items-center gap-2 flex-wrap">
    <span class="text-xs font-mono uppercase tracking-widest text-neon-magenta/90">热门:</span>
    <button
      v-for="tagStat in tagsStore.hotTags.slice(0, 8)"
      :key="tagStat.tag"
      @click="toggleTag(tagStat.tag)"
      class="px-2 py-0.5 text-xs font-mono border transition-all duration-200 uppercase tracking-wider"
      :class="activeTag === tagStat.tag.toLowerCase()
        ? 'bg-neon-cyan/20 border-neon-cyan text-neon-cyan shadow-neon-cyan'
        : 'bg-transparent border-border-dim text-chrome/60 hover:border-neon-cyan hover:text-neon-cyan hover:shadow-neon-cyan'"
    >
      {{ tagStat.tag }}
    </button>
  </div>
</template>
