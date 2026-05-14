<script setup lang="ts">
import type { Genre } from '@/types'
import GenreNode from './GenreNode.vue'

defineProps<{
  genres: Genre[]
}>()
</script>

<template>
  <div class="relative pl-4 mt-4">
    <!-- Bauhaus vertical line -->
    <div class="absolute left-2 top-0 bottom-0 w-1 bg-foreground dark:bg-dark-border"></div>
    
    <div v-for="genre in genres" :key="genre.id" class="mb-2">
      <GenreNode :genre="genre" />
    </div>
  </div>
</template>
