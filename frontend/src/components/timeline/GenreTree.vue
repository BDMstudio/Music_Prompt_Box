<script setup lang="ts">
import type { Genre } from '@/types'
import GenreNode from './GenreNode.vue'

defineProps<{
  genres: Genre[]
}>()
</script>

<template>
  <div class="relative pl-4">
    <div class="absolute left-2 top-0 bottom-0 w-0.5 bg-zinc-700"></div>
    
    <div v-for="genre in genres" :key="genre.id" class="mb-2">
      <GenreNode :genre="genre" />
    </div>
  </div>
</template>
