<script setup lang="ts">
import { computed, watch } from 'vue'
import SearchBox from '../common/SearchBox.vue'
import HotTags from '../tags/HotTags.vue'
import StyleGrid from '../cards/StyleGrid.vue'
import { useStylesStore } from '@/stores/styles'
import { useGenresStore } from '@/stores/genres'

const stylesStore = useStylesStore()
const genresStore = useGenresStore()

const title = computed(() => {
  if (genresStore.selectedGenre) {
    return `${genresStore.selectedGenre.name} 风格`
  }
  return '全部风格'
})

const subtitle = computed(() => {
  return `共 ${stylesStore.total} 个风格`
})

function handleSearch(query: string) {
  stylesStore.setSearch(query)
  stylesStore.loadStyles()
}

watch(() => stylesStore.page, () => {
  stylesStore.loadStyles()
})
</script>

<template>
  <main class="flex-1 overflow-y-auto p-6">
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-2xl font-bold text-white">{{ title }}</h1>
          <p class="text-sm text-text-sub">{{ subtitle }}</p>
        </div>
      </div>
      
      <div class="flex items-center gap-4 flex-wrap">
        <SearchBox @search="handleSearch" />
        <HotTags />
      </div>
    </div>

    <StyleGrid />
  </main>
</template>
