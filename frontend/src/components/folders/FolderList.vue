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
  <div class="absolute right-0 top-full mt-2 w-72 border-2 border-neon-cyan bg-black/90 shadow-neon-cyan-lg z-50 overflow-hidden">
    <!-- Title bar with window chrome -->
    <div class="flex items-center justify-between bg-neon-cyan/10 border-b border-neon-cyan px-4 py-2">
      <div class="flex items-center gap-2">
        <div class="h-2.5 w-2.5 rounded-full bg-neon-magenta"></div>
        <div class="h-2.5 w-2.5 rounded-full bg-neon-cyan"></div>
        <div class="h-2.5 w-2.5 rounded-full bg-neon-orange"></div>
      </div>
      <span class="text-xs font-mono text-neon-cyan/60">folders.exe</span>
      <button
        @click="showCreateInput = true"
        class="text-xs font-mono text-neon-magenta hover:text-white"
      >
        + 新建
      </button>
    </div>

    <!-- Folder list -->
    <div class="max-h-64 overflow-y-auto">
      <div
        @click="filterByFolder(null)"
        class="px-3 py-2 hover:bg-neon-cyan/10 cursor-pointer text-sm font-mono text-chrome flex items-center gap-2 border-b border-border-dim"
      >
        <svg class="w-4 h-4 text-neon-cyan/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
        </svg>
        > 全部风格
      </div>

      <div
        v-for="folder in foldersStore.folders"
        :key="folder.id"
        class="group px-3 py-2 hover:bg-neon-cyan/10 cursor-pointer border-b border-border-dim/50"
      >
        <div v-if="editingId === folder.id" class="flex items-center gap-2">
          <input
            v-model="editingName"
            @keyup.enter="saveEdit"
            @blur="saveEdit"
            class="flex-1 border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-sm px-1 py-1 focus:outline-none focus:border-neon-cyan"
            autofocus
          />
        </div>
        <div v-else class="flex items-center justify-between" @click="filterByFolder(folder.id)">
          <div class="flex items-center gap-2 text-sm font-mono text-chrome">
            <svg class="w-4 h-4 text-neon-orange" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
            </svg>
            {{ folder.name }}
            <span class="text-text-sub">({{ folder.style_count }})</span>
          </div>
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100">
            <button
              @click.stop="startEdit(folder.id, folder.name)"
              class="p-1 hover:bg-neon-cyan/20 text-text-sub"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
            </button>
            <button
              @click.stop="removeFolder(folder.id)"
              class="p-1 hover:bg-neon-magenta/30 text-text-sub hover:text-neon-magenta"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="foldersStore.folders.length === 0 && !showCreateInput" class="px-3 py-4 text-center text-sm text-text-sub font-mono">
        暂无收藏夹
      </div>
    </div>

    <!-- Create input -->
    <div v-if="showCreateInput" class="p-3 border-t-2 border-neon-cyan bg-void">
      <div class="flex items-center gap-2">
        <input
          v-model="newFolderName"
          @keyup.enter="createFolder"
          placeholder="收藏夹名称"
          class="flex-1 border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-sm px-1 py-1
                 placeholder:text-neon-magenta/40 focus:outline-none focus:border-neon-cyan"
          autofocus
        />
        <button
          @click="createFolder"
          class="-skew-x-12 border-2 border-neon-magenta bg-neon-magenta text-white font-mono text-xs uppercase tracking-wider px-2 py-1
                 hover:skew-x-0 hover:shadow-neon-magenta transition-all duration-200"
        >
          <span class="inline-block skew-x-12">创建</span>
        </button>
        <button
          @click="showCreateInput = false"
          class="p-1 text-text-sub hover:text-neon-magenta"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Status bar -->
    <div class="border-t-2 border-border-dim bg-void px-3 py-1 text-text-sub text-xs font-mono flex justify-between">
      <span>{{ foldersStore.folders.length }} 个收藏夹</span>
      <span class="text-neon-cyan/50">ready</span>
    </div>
  </div>
</template>
