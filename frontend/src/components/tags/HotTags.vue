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
    <span class="text-xs text-text-sub">热门:</span>
    <button
      v-for="tagStat in tagsStore.hotTags.slice(0, 8)"
      :key="tagStat.tag"
      @click="searchByTag(tagStat.tag)"
      class="px-2 py-0.5 text-xs bg-zinc-800 hover:bg-accent/30 text-zinc-400 hover:text-accent rounded transition"
    >
      {{ tagStat.tag }}
    </button>
  </div>
</template>
