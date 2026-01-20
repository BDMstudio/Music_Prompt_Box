import apiClient from './client'
import type { TagStat } from '@/types'

export async function fetchHotTags(limit: number = 20): Promise<TagStat[]> {
  const response = await apiClient.get<TagStat[]>('/tags/hot', { params: { limit } })
  return response.data
}

export async function recordTagCopies(tags: string[]): Promise<void> {
  await apiClient.post('/tags/copy', { tags })
}
