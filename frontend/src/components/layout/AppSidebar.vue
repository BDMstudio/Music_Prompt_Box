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
  <aside class="w-[320px] flex-shrink-0 bg-sidebar-bg border-r border-border overflow-y-auto">
    <div class="p-4 border-b border-border">
      <h2 class="text-white font-semibold mb-1">流派时间线</h2>
      <p class="text-xs text-text-sub">选择流派筛选风格卡片</p>
    </div>
    
    <div class="p-4">
      <button
        @click="genresStore.selectGenre(null)"
        class="w-full text-left px-3 py-2 rounded-lg text-sm mb-4 transition"
        :class="genresStore.selectedGenreId === null ? 'bg-accent/20 text-accent' : 'text-text-sub hover:bg-zinc-800'"
      >
        查看全部
      </button>
      
      <GenreTree :genres="genresStore.genres" />
    </div>
  </aside>
</template>
