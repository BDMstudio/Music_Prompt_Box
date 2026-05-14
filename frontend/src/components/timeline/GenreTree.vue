<script setup lang="ts">
import type { Genre } from '@/types'
import GenreNode from './GenreNode.vue'

defineProps<{
  genres: Genre[]
}>()
</script>

<template>
  <div class="relative mt-4">
    
    <div v-for="genre in genres" :key="genre.id" class="mb-2">
      <GenreNode :genre="genre" />
    </div>
  </div>
</template>
