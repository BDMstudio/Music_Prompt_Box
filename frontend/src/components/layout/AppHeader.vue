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
  <header class="h-[60px] flex-shrink-0 bg-void/90 backdrop-blur-md border-b-2 border-border-dim flex items-center justify-between px-4 md:px-4 overflow-hidden">
    <!-- Logo -->
    <div class="flex items-center gap-2 md:gap-3 min-w-0">
      <div class="flex items-center gap-1.5 flex-shrink-0">
        <div class="w-3 h-3 rounded-full bg-neon-magenta"></div>
        <div class="w-3 h-3 rounded-full bg-neon-cyan"></div>
        <div class="w-3 h-3 rounded-full bg-neon-orange"></div>
      </div>
      <span class="font-heading font-bold text-sm md:text-lg uppercase tracking-wider gradient-text truncate">
        Music Prompt Box
      </span>
    </div>

    <!-- Action buttons -->
    <div class="flex items-center gap-2 md:gap-3 flex-shrink-0">
      <div class="relative">
        <button
          @click="toggleFolders"
          class="-skew-x-6 md:-skew-x-12 border-2 border-neon-cyan bg-transparent text-neon-cyan rounded-none
                 uppercase tracking-wider font-mono text-xs md:text-sm px-2 md:px-4 py-1.5 md:py-2
                 hover:skew-x-0 hover:bg-neon-cyan hover:text-void hover:shadow-neon-cyan
                 transition-all duration-200 flex items-center gap-1 md:gap-2"
        >
          <span class="inline-block skew-x-6 md:skew-x-12 flex items-center gap-1 md:gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"/>
            </svg>
            <span class="hidden sm:inline">收藏夹</span>
          </span>
        </button>
        
        <FolderList v-if="showFolders" @close="showFolders = false" />
      </div>

      <button
        @click="openAddModal"
        class="-skew-x-6 md:-skew-x-12 border-2 border-neon-magenta bg-neon-magenta text-white rounded-none
               uppercase tracking-wider font-mono text-xs md:text-sm px-2 md:px-4 py-1.5 md:py-2
               hover:skew-x-0 hover:scale-105 hover:opacity-90 hover:shadow-neon-magenta-lg
               transition-all duration-200 flex items-center gap-1 md:gap-2"
      >
        <span class="inline-block skew-x-6 md:skew-x-12 flex items-center gap-1 md:gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          <span class="hidden sm:inline">添加风格</span>
        </span>
      </button>
    </div>

    <StyleFormModal v-if="showAddModal" @close="showAddModal = false" />
  </header>
</template>
