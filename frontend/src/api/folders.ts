import apiClient from './client'
import type { Folder, FolderCreateInput } from '@/types'

export async function fetchFolders(): Promise<Folder[]> {
  const response = await apiClient.get<Folder[]>('/folders')
  return response.data
}

export async function createFolder(data: FolderCreateInput): Promise<Folder> {
  const response = await apiClient.post<Folder>('/folders', data)
  return response.data
}

export async function updateFolder(id: string, data: Partial<FolderCreateInput>): Promise<Folder> {
  const response = await apiClient.put<Folder>(`/folders/${id}`, data)
  return response.data
}

export async function deleteFolder(id: string): Promise<void> {
  await apiClient.delete(`/folders/${id}`)
}

export async function addStyleToFolder(folderId: string, styleId: string): Promise<void> {
  await apiClient.post(`/folders/${folderId}/styles`, { style_id: styleId })
}

export async function removeStyleFromFolder(folderId: string, styleId: string): Promise<void> {
  await apiClient.delete(`/folders/${folderId}/styles/${styleId}`)
}
