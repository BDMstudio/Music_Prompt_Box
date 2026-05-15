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
  <aside class="w-[320px] flex-shrink-0 bg-sidebar-bg border-r-2 border-border-dim overflow-y-auto">
    <!-- Terminal-style header -->
    <div class="border-b border-neon-cyan/30">
      <div class="flex items-center gap-2 px-4 py-2 bg-neon-cyan/5 border-b border-neon-cyan/20">
        <div class="h-3.5 w-0.5 rounded-full bg-neon-magenta"></div>
        <span class="ml-2 text-xs text-neon-cyan/80 font-mono">genre_tree.exe</span>
      </div>
      <div class="p-4">
        <h2 class="font-heading font-bold text-lg uppercase tracking-wider text-neon-cyan glow-text-cyan">流派时间线</h2>
        <p class="text-xs text-chrome/60 mt-1 font-mono">&gt; 选择流派筛选风格卡片</p>
      </div>
    </div>
    
    <!-- View All button -->
    <div class="p-4">
      <button
        @click="genresStore.selectGenre(null)"
        class="w-full text-left px-3 py-2 border-2 font-mono text-sm uppercase tracking-wider transition-all duration-200"
        :class="genresStore.selectedGenreId === null
          ? 'border-neon-magenta bg-neon-magenta/20 text-neon-magenta shadow-neon-magenta'
          : 'border-border-dim text-chrome/70 hover:border-neon-cyan hover:text-neon-cyan'"
      >
        > 查看全部
      </button>
      
      <GenreTree :genres="genresStore.genres" />
    </div>
  </aside>
</template>
