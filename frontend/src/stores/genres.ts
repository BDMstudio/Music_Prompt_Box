import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Genre } from '@/types'
import { fetchGenres } from '@/api/genres'

export const useGenresStore = defineStore('genres', () => {
  const genres = ref<Genre[]>([])
  const selectedGenreId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const selectedGenre = computed(() => {
    if (!selectedGenreId.value) return null
    return findGenreById(genres.value, selectedGenreId.value)
  })

  function findGenreById(genreList: Genre[], id: string): Genre | null {
    for (const genre of genreList) {
      if (genre.id === id) return genre
      if (genre.children?.length) {
        const found = findGenreById(genre.children, id)
        if (found) return found
      }
    }
    return null
  }

  function getAllDescendantIds(genre: Genre): string[] {
    const ids = [genre.id]
    for (const child of genre.children || []) {
      ids.push(...getAllDescendantIds(child))
    }
    return ids
  }

  const selectedGenreIds = computed(() => {
    if (!selectedGenre.value) return []
    return getAllDescendantIds(selectedGenre.value)
  })

  async function loadGenres() {
    loading.value = true
    error.value = null
    try {
      genres.value = await fetchGenres()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load genres'
    } finally {
      loading.value = false
    }
  }

  function selectGenre(id: string | null) {
    selectedGenreId.value = id
  }

  return {
    genres,
    selectedGenreId,
    selectedGenre,
    selectedGenreIds,
    loading,
    error,
    loadGenres,
    selectGenre,
  }
})
