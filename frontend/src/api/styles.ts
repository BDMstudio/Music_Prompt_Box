import apiClient from './client'
import type { Style, StyleListResponse, StyleCreateInput, StyleUpdateInput } from '@/types'

interface FetchStylesParams {
  genre_id?: string
  search?: string
  folder_id?: string
  page?: number
  size?: number
}

export async function fetchStyles(params: FetchStylesParams = {}): Promise<StyleListResponse> {
  const response = await apiClient.get<StyleListResponse>('/styles', { params })
  return response.data
}

export async function fetchStyle(id: string): Promise<Style> {
  const response = await apiClient.get<Style>(`/styles/${id}`)
  return response.data
}

export async function createStyle(data: StyleCreateInput): Promise<Style> {
  const response = await apiClient.post<Style>('/styles', data)
  return response.data
}

export async function updateStyle(id: string, data: StyleUpdateInput): Promise<Style> {
  const response = await apiClient.put<Style>(`/styles/${id}`, data)
  return response.data
}

export async function deleteStyle(id: string): Promise<void> {
  await apiClient.delete(`/styles/${id}`)
}

export async function incrementStyleCopyCount(id: string): Promise<void> {
  await apiClient.post(`/styles/${id}/copy`)
}
