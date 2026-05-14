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
  <main class="flex-1 overflow-y-auto p-6 bg-dot-grid">
    <!-- Title area -->
    <div class="mb-6">
      <div class="flex items-end justify-between mb-4">
        <div>
          <h1 class="text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-[0.9] text-foreground dark:text-dark-text-main">{{ title }}</h1>
          <p class="text-sm font-bold uppercase tracking-widest text-text-sub dark:text-dark-text-sub mt-2">{{ subtitle }}</p>
        </div>
        <!-- Geometric decoration -->
        <div class="hidden sm:flex items-center gap-2">
          <div class="w-6 h-6 geo-square bg-primary-yellow border-2 border-foreground dark:border-dark-border rotate-45"></div>
          <div class="w-6 h-6 geo-circle bg-primary-red"></div>
        </div>
      </div>
      
      <!-- Search + tags row -->
      <div class="flex items-center gap-4 flex-wrap">
        <SearchBox @search="handleSearch" />
        <HotTags />
      </div>
    </div>

    <StyleGrid />
  </main>
</template>
