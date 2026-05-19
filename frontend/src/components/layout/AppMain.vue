<script setup lang="ts">
import { computed, watch } from 'vue'
import SearchBox from '../common/SearchBox.vue'
import HotTags from '../tags/HotTags.vue'
import StyleGrid from '../cards/StyleGrid.vue'
import { useStylesStore } from '@/stores/styles'
import { useGenresStore } from '@/stores/genres'
import { useAudio } from '@/composables/useAudio'

const stylesStore = useStylesStore()
const genresStore = useGenresStore()
const { isPlaying } = useAudio()

const title = computed(() => {
  if (genresStore.selectedGenre) {
    return `${genresStore.selectedGenre.name} `
  }
  return 'ALL styles'
})

const subtitle = computed(() => {
  return `> 共 ${stylesStore.total} 个风格`
})

const contentClass = computed(() => {
  return isPlaying.value ? 'pb-16' : ''
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
  <main class="flex-1 overflow-y-auto overflow-x-hidden p-4 md:p-6 relative min-w-0">
    <!-- Perspective grid background — isolated in overflow-hidden container -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute bottom-0 left-0 right-0 h-[300px] perspective-grid opacity-20"></div>
    </div>

    <div class="relative z-10" :class="contentClass">
      <!-- Title area -->
      <div class="mb-6">
        <div class="flex items-end justify-between mb-4">
          <div class="relative">
            <h1 class="font-heading font-black text-3xl sm:text-4xl lg:text-5xl uppercase tracking-wider gradient-text leading-tight">{{ title }}</h1>
            <div class="crt-scanlines-strong absolute inset-0 pointer-events-none"></div>
            <p class="text-sm text-neon-magenta/80 font-mono mt-2 tracking-wider">{{ subtitle }}</p>
          </div>
        </div>
        
        <!-- Search + tags row -->
        <div class="flex items-center gap-4 flex-wrap">
          <SearchBox @search="handleSearch" />
          <HotTags />
        </div>
      </div>

      <StyleGrid />
    </div>
  </main>
</template>
