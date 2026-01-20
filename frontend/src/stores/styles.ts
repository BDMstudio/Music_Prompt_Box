import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Style, StyleCreateInput, StyleUpdateInput } from '@/types'
import { fetchStyles, createStyle, updateStyle, deleteStyle, incrementStyleCopyCount } from '@/api/styles'

export const useStylesStore = defineStore('styles', () => {
  const styles = ref<Style[]>([])
  const total = ref(0)
  const page = ref(1)
  const size = ref(20)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const searchQuery = ref('')
  const filterGenreId = ref<string | null>(null)
  const filterFolderId = ref<string | null>(null)

  async function loadStyles() {
    loading.value = true
    error.value = null
    try {
      const params: Record<string, unknown> = {
        page: page.value,
        size: size.value,
      }
      if (searchQuery.value) params.search = searchQuery.value
      if (filterGenreId.value) params.genre_id = filterGenreId.value
      if (filterFolderId.value) params.folder_id = filterFolderId.value

      const response = await fetchStyles(params)
      styles.value = response.items
      total.value = response.total
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load styles'
    } finally {
      loading.value = false
    }
  }

  async function addStyle(data: StyleCreateInput): Promise<Style | null> {
    try {
      const newStyle = await createStyle(data)
      await loadStyles()
      return newStyle
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create style'
      return null
    }
  }

  async function editStyle(id: string, data: StyleUpdateInput): Promise<Style | null> {
    try {
      const updatedStyle = await updateStyle(id, data)
      const index = styles.value.findIndex(s => s.id === id)
      if (index !== -1) {
        styles.value[index] = updatedStyle
      }
      return updatedStyle
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update style'
      return null
    }
  }

  async function removeStyle(id: string): Promise<boolean> {
    try {
      await deleteStyle(id)
      styles.value = styles.value.filter(s => s.id !== id)
      total.value -= 1
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete style'
      return false
    }
  }

  async function recordCopy(id: string) {
    try {
      await incrementStyleCopyCount(id)
      const style = styles.value.find(s => s.id === id)
      if (style) {
        style.copy_count += 1
      }
    } catch {
    }
  }

  function setSearch(query: string) {
    searchQuery.value = query
    page.value = 1
  }

  function setGenreFilter(genreId: string | null) {
    filterGenreId.value = genreId
    page.value = 1
  }

  function setFolderFilter(folderId: string | null) {
    filterFolderId.value = folderId
    page.value = 1
  }

  function setPage(newPage: number) {
    page.value = newPage
  }

  return {
    styles,
    total,
    page,
    size,
    loading,
    error,
    searchQuery,
    filterGenreId,
    filterFolderId,
    loadStyles,
    addStyle,
    editStyle,
    removeStyle,
    recordCopy,
    setSearch,
    setGenreFilter,
    setFolderFilter,
    setPage,
  }
})
