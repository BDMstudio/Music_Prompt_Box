<script setup lang="ts">
import { ref } from 'vue'
import { useFoldersStore } from '@/stores/folders'
import { useStylesStore } from '@/stores/styles'

const emit = defineEmits<{
  close: []
}>()

const foldersStore = useFoldersStore()
const stylesStore = useStylesStore()

const showCreateInput = ref(false)
const newFolderName = ref('')
const editingId = ref<string | null>(null)
const editingName = ref('')

async function createFolder() {
  if (!newFolderName.value.trim()) return
  await foldersStore.addFolder({ name: newFolderName.value })
  newFolderName.value = ''
  showCreateInput.value = false
}

function startEdit(id: string, name: string) {
  editingId.value = id
  editingName.value = name
}

async function saveEdit() {
  if (!editingId.value || !editingName.value.trim()) return
  await foldersStore.editFolder(editingId.value, { name: editingName.value })
  editingId.value = null
}

async function removeFolder(id: string) {
  await foldersStore.removeFolder(id)
}

function filterByFolder(folderId: string | null) {
  stylesStore.setFolderFilter(folderId)
  stylesStore.loadStyles()
  emit('close')
}
</script>

<template>
  <div class="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-dark-surface border-4 border-foreground dark:border-dark-border shadow-hard-lg dark:shadow-dark-hard-lg z-50 overflow-hidden transition-colors duration-300">
    <!-- Header -->
    <div class="p-3 bg-primary-yellow border-b-4 border-foreground dark:border-dark-border">
      <div class="flex items-center justify-between">
        <span class="text-sm font-black uppercase tracking-wider text-foreground">收藏夹</span>
        <button
          @click="showCreateInput = true"
          class="text-xs font-bold uppercase tracking-widest text-foreground hover:text-primary-red"
        >
          + 新建
        </button>
      </div>
    </div>

    <!-- Folder list -->
    <div class="max-h-64 overflow-y-auto">
      <div
        @click="filterByFolder(null)"
        class="px-3 py-2 hover:bg-primary-yellow/30 cursor-pointer text-sm font-bold uppercase tracking-wider flex items-center gap-2 border-b-2 border-foreground/10 dark:border-dark-border/30 text-foreground dark:text-dark-text-main"
      >
        <svg class="w-4 h-4 text-foreground dark:text-dark-text-main" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
        </svg>
        全部风格
      </div>

      <div
        v-for="folder in foldersStore.folders"
        :key="folder.id"
        class="group px-3 py-2 hover:bg-muted dark:hover:bg-dark-muted cursor-pointer border-b-2 border-foreground/5 dark:border-dark-border/10"
      >
        <div v-if="editingId === folder.id" class="flex items-center gap-2">
          <input
            v-model="editingName"
            @keyup.enter="saveEdit"
            @blur="saveEdit"
            class="flex-1 px-2 py-1 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-sm font-medium text-foreground dark:text-dark-text-main focus:outline-none focus:border-primary-red"
            autofocus
          />
        </div>
        <div v-else class="flex items-center justify-between" @click="filterByFolder(folder.id)">
          <div class="flex items-center gap-2 text-sm font-bold text-foreground dark:text-dark-text-main">
            <svg class="w-4 h-4 text-primary-yellow" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
            </svg>
            {{ folder.name }}
            <span class="text-text-sub dark:text-dark-text-sub font-medium">({{ folder.style_count }})</span>
          </div>
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100">
            <button
              @click.stop="startEdit(folder.id, folder.name)"
              class="p-1 hover:bg-primary-yellow/30 text-foreground dark:text-dark-text-main"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
            </button>
            <button
              @click.stop="removeFolder(folder.id)"
              class="p-1 hover:bg-primary-red hover:text-white text-foreground dark:text-dark-text-main"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="foldersStore.folders.length === 0 && !showCreateInput" class="px-3 py-4 text-center text-sm text-text-sub dark:text-dark-text-sub font-medium">
        暂无收藏夹
      </div>
    </div>

    <!-- Create input -->
    <div v-if="showCreateInput" class="p-3 border-t-4 border-foreground dark:border-dark-border bg-background dark:bg-dark-surface-alt">
      <div class="flex items-center gap-2">
        <input
          v-model="newFolderName"
          @keyup.enter="createFolder"
          placeholder="收藏夹名称"
          class="flex-1 px-2 py-1 bg-white dark:bg-dark-surface border-2 border-foreground dark:border-dark-border text-sm font-medium text-foreground dark:text-dark-text-main focus:outline-none focus:border-primary-blue"
          autofocus
        />
        <button
          @click="createFolder"
          class="px-3 py-1 bg-primary-blue text-white border-2 border-foreground dark:border-dark-border font-bold text-xs uppercase tracking-wider
                 hover:bg-primary-blue/90 active:translate-x-[1px] active:translate-y-[1px] active:shadow-none shadow-hard-sm dark:shadow-dark-hard-sm transition-all"
        >
          创建
        </button>
        <button
          @click="showCreateInput = false"
          class="p-1 text-text-sub dark:text-dark-text-sub hover:text-foreground dark:hover:text-dark-text-main"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
