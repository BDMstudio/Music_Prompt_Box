<script setup lang="ts">
import { watch } from 'vue'
import GenreTree from '../timeline/GenreTree.vue'
import { useGenresStore } from '@/stores/genres'
import { useStylesStore } from '@/stores/styles'

const genresStore = useGenresStore()
const stylesStore = useStylesStore()

watch(() => genresStore.selectedGenreId, (newId) => {
  stylesStore.setGenreFilter(newId)
  stylesStore.loadStyles()
})
</script>

<template>
  <aside class="w-[320px] flex-shrink-0 bg-white dark:bg-dark-surface border-r-4 border-foreground dark:border-dark-border overflow-y-auto transition-colors duration-300">
    <!-- Sidebar header -->
    <div class="p-4 border-b-4 border-foreground dark:border-dark-border bg-primary-blue">
      <h2 class="text-white font-black uppercase tracking-tighter text-lg">流派时间线</h2>
      <p class="text-xs text-white/70 font-medium mt-1">选择流派筛选风格卡片</p>
    </div>
    
    <!-- View All button -->
    <div class="p-4">
      <button
        @click="genresStore.selectGenre(null)"
        class="w-full text-left px-4 py-2 border-2 font-bold uppercase tracking-wider text-sm transition-all duration-200
               border-foreground dark:border-dark-border"
        :class="genresStore.selectedGenreId === null
          ? 'bg-primary-red text-white shadow-hard-sm dark:shadow-dark-hard-sm'
          : 'bg-white dark:bg-dark-surface text-foreground dark:text-dark-text-main hover:bg-muted dark:hover:bg-dark-muted'"
      >
        查看全部
      </button>
      
      <GenreTree :genres="genresStore.genres" />
    </div>
  </aside>
</template>
