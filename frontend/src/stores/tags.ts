import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TagStat } from '@/types'
import { fetchHotTags, recordTagCopies } from '@/api/tags'

export const useTagsStore = defineStore('tags', () => {
  const hotTags = ref<TagStat[]>([])
  const loading = ref(false)

  async function loadHotTags(limit: number = 20) {
    loading.value = true
    try {
      hotTags.value = await fetchHotTags(limit)
    } catch {
    } finally {
      loading.value = false
    }
  }

  async function recordCopies(tags: string[]) {
    try {
      await recordTagCopies(tags)
      await loadHotTags()
    } catch {
    }
  }

  return {
    hotTags,
    loading,
    loadHotTags,
    recordCopies,
  }
})
