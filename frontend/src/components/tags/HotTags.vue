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
    <span class="text-xs font-bold uppercase tracking-widest text-text-sub dark:text-dark-text-sub">热门:</span>
    <button
      v-for="tagStat in tagsStore.hotTags.slice(0, 8)"
      :key="tagStat.tag"
      @click="searchByTag(tagStat.tag)"
      class="px-2 py-0.5 text-xs font-bold uppercase tracking-wider bg-white dark:bg-dark-surface border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main
             hover:bg-primary-blue hover:text-white transition-all duration-200"
    >
      {{ tagStat.tag }}
    </button>
  </div>
</template>
