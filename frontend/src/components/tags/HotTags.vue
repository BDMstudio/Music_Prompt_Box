<script setup lang="ts">
import { useTagsStore } from '@/stores/tags'
import { useStylesStore } from '@/stores/styles'

const tagsStore = useTagsStore()
const stylesStore = useStylesStore()

function searchByTag(tag: string) {
  stylesStore.setSearch(tag)
  stylesStore.loadStyles()
}
</script>

<template>
  <div v-if="tagsStore.hotTags.length > 0" class="flex items-center gap-2 flex-wrap">
    <span class="text-xs font-mono uppercase tracking-widest text-neon-magenta/50">热门:</span>
    <button
      v-for="tagStat in tagsStore.hotTags.slice(0, 8)"
      :key="tagStat.tag"
      @click="searchByTag(tagStat.tag)"
      class="px-2 py-0.5 text-xs font-mono bg-transparent border border-border-dim text-text-sub
             hover:border-neon-cyan hover:text-neon-cyan hover:shadow-neon-cyan
             transition-all duration-200 uppercase tracking-wider"
    >
      {{ tagStat.tag }}
    </button>
  </div>
</template>
