<script setup lang="ts">
import { ref } from 'vue'
import FolderList from '../folders/FolderList.vue'
import StyleFormModal from '../cards/StyleFormModal.vue'

const showFolders = ref(false)
const showAddModal = ref(false)

function toggleFolders() {
  showFolders.value = !showFolders.value
}

function openAddModal() {
  showAddModal.value = true
}
</script>

<template>
  <header class="h-[60px] flex-shrink-0 bg-sidebar-bg/80 backdrop-blur-xl border-b border-border flex items-center justify-between px-4">
    <div class="flex items-center gap-2">
      <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
      </svg>
      <span class="text-lg font-extrabold bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">
        Music Prompt Box
      </span>
    </div>

    <div class="flex items-center gap-2">
      <div class="relative">
        <button
          @click="toggleFolders"
          class="px-3 py-1.5 text-sm border border-zinc-700 rounded-lg hover:bg-zinc-800 transition flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"/>
          </svg>
          收藏夹
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        
        <FolderList v-if="showFolders" @close="showFolders = false" />
      </div>

      <button
        @click="openAddModal"
        class="px-3 py-1.5 text-sm bg-accent hover:bg-accent/80 rounded-lg transition flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        添加风格
      </button>
    </div>

    <StyleFormModal v-if="showAddModal" @close="showAddModal = false" />
  </header>
</template>
