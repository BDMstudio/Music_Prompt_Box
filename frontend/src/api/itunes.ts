import apiClient from './client'
import type { ITuneSearchResponse } from '@/types'

export async function searchITunes(
  term: string,
  options: {
    country?: string
    limit?: number
    genre?: string
  } = {}
): Promise<ITuneSearchResponse> {
  const params: Record<string, string | number> = {
    term,
    country: options.country || 'US',
    limit: options.limit || 10,
  }
  if (options.genre) {
    params.genre = options.genre
  }
  const response = await apiClient.get<ITuneSearchResponse>('/itunes/search', { params })
  return response.data
}

export async function lookupITuneTrack(
  trackId: number
): Promise<ITuneSearchResponse> {
  const response = await apiClient.get<ITuneSearchResponse>('/itunes/lookup', {
    params: { id: trackId },
  })
  return response.data
}
