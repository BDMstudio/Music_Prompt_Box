import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Folder, FolderCreateInput } from '@/types'
import { fetchFolders, createFolder, updateFolder, deleteFolder, addStyleToFolder, removeStyleFromFolder } from '@/api/folders'

export const useFoldersStore = defineStore('folders', () => {
  const folders = ref<Folder[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadFolders() {
    loading.value = true
    error.value = null
    try {
      folders.value = await fetchFolders()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load folders'
    } finally {
      loading.value = false
    }
  }

  async function addFolder(data: FolderCreateInput): Promise<Folder | null> {
    try {
      const newFolder = await createFolder(data)
      folders.value.push(newFolder)
      return newFolder
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create folder'
      return null
    }
  }

  async function editFolder(id: string, data: Partial<FolderCreateInput>): Promise<Folder | null> {
    try {
      const updatedFolder = await updateFolder(id, data)
      const index = folders.value.findIndex(f => f.id === id)
      if (index !== -1) {
        folders.value[index] = updatedFolder
      }
      return updatedFolder
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update folder'
      return null
    }
  }

  async function removeFolder(id: string): Promise<boolean> {
    try {
      await deleteFolder(id)
      folders.value = folders.value.filter(f => f.id !== id)
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete folder'
      return false
    }
  }

  async function addToFolder(folderId: string, styleId: string): Promise<boolean> {
    try {
      await addStyleToFolder(folderId, styleId)
      const folder = folders.value.find(f => f.id === folderId)
      if (folder) {
        folder.style_count += 1
      }
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to add style to folder'
      return false
    }
  }

  async function removeFromFolder(folderId: string, styleId: string): Promise<boolean> {
    try {
      await removeStyleFromFolder(folderId, styleId)
      const folder = folders.value.find(f => f.id === folderId)
      if (folder && folder.style_count > 0) {
        folder.style_count -= 1
      }
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to remove style from folder'
      return false
    }
  }

  return {
    folders,
    loading,
    error,
    loadFolders,
    addFolder,
    editFolder,
    removeFolder,
    addToFolder,
    removeFromFolder,
  }
})
