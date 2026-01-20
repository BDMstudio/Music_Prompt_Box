import apiClient from './client'
import type { Genre } from '@/types'

export async function fetchGenres(): Promise<Genre[]> {
  const response = await apiClient.get<Genre[]>('/genres')
  return response.data
}

export async function createGenre(data: Partial<Genre> & { id: string; name: string }): Promise<Genre> {
  const response = await apiClient.post<Genre>('/genres', data)
  return response.data
}

export async function updateGenre(id: string, data: Partial<Genre>): Promise<Genre> {
  const response = await apiClient.put<Genre>(`/genres/${id}`, data)
  return response.data
}

export async function deleteGenre(id: string): Promise<void> {
  await apiClient.delete(`/genres/${id}`)
}
