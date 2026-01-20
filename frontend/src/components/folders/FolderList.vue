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
  <div class="absolute right-0 top-full mt-2 w-64 bg-zinc-900 border border-zinc-700 rounded-xl shadow-2xl z-50 overflow-hidden">
    <div class="p-3 border-b border-zinc-800">
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">收藏夹</span>
        <button
          @click="showCreateInput = true"
          class="text-xs text-accent hover:underline"
        >
          新建
        </button>
      </div>
    </div>

    <div class="max-h-64 overflow-y-auto">
      <div
        @click="filterByFolder(null)"
        class="px-3 py-2 hover:bg-zinc-800 cursor-pointer text-sm flex items-center gap-2"
      >
        <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
        </svg>
        全部风格
      </div>

      <div
        v-for="folder in foldersStore.folders"
        :key="folder.id"
        class="group px-3 py-2 hover:bg-zinc-800 cursor-pointer"
      >
        <div v-if="editingId === folder.id" class="flex items-center gap-2">
          <input
            v-model="editingName"
            @keyup.enter="saveEdit"
            @blur="saveEdit"
            class="flex-1 px-2 py-1 bg-zinc-800 border border-zinc-600 rounded text-sm"
            autofocus
          />
        </div>
        <div v-else class="flex items-center justify-between" @click="filterByFolder(folder.id)">
          <div class="flex items-center gap-2 text-sm">
            <svg class="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
            </svg>
            {{ folder.name }}
            <span class="text-zinc-600">({{ folder.style_count }})</span>
          </div>
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100">
            <button
              @click.stop="startEdit(folder.id, folder.name)"
              class="p-1 hover:bg-zinc-700 rounded"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
            </button>
            <button
              @click.stop="removeFolder(folder.id)"
              class="p-1 hover:bg-red-900/50 rounded text-red-400"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="foldersStore.folders.length === 0 && !showCreateInput" class="px-3 py-4 text-center text-sm text-zinc-500">
        暂无收藏夹
      </div>
    </div>

    <div v-if="showCreateInput" class="p-3 border-t border-zinc-800">
      <div class="flex items-center gap-2">
        <input
          v-model="newFolderName"
          @keyup.enter="createFolder"
          placeholder="收藏夹名称"
          class="flex-1 px-2 py-1 bg-zinc-800 border border-zinc-600 rounded text-sm focus:outline-none focus:border-accent"
          autofocus
        />
        <button
          @click="createFolder"
          class="px-2 py-1 bg-accent rounded text-xs hover:bg-accent/80"
        >
          创建
        </button>
        <button
          @click="showCreateInput = false"
          class="p-1 text-zinc-500 hover:text-white"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
