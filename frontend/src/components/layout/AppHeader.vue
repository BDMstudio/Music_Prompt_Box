<script setup lang="ts">
import { ref } from 'vue'
import FolderList from '../folders/FolderList.vue'
import StyleFormModal from '../cards/StyleFormModal.vue'
import { useTheme } from '@/composables/useTheme'

const showFolders = ref(false)
const showAddModal = ref(false)
const { isDark, toggle } = useTheme()

function toggleFolders() {
  showFolders.value = !showFolders.value
}

function openAddModal() {
  showAddModal.value = true
}
</script>

<template>
  <header class="h-[60px] flex-shrink-0 bg-white dark:bg-dark-surface border-b-4 border-foreground dark:border-dark-border flex items-center justify-between px-6 transition-colors duration-300">
    <!-- Logo: geometric shapes + title -->
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1">
        <div class="w-4 h-4 geo-circle bg-primary-red"></div>
        <div class="w-4 h-4 geo-square bg-primary-blue"></div>
        <div class="w-4 h-4 geo-triangle bg-primary-yellow"></div>
      </div>
      <span class="text-lg font-black uppercase tracking-tighter text-foreground dark:text-dark-text-main">
        Music Prompt Box
      </span>
    </div>

    <!-- Action buttons -->
    <div class="flex items-center gap-3">
      <!-- Dark mode toggle -->
      <button
        @click="toggle"
        class="w-10 h-10 flex items-center justify-center border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface shadow-hard-sm dark:shadow-dark-hard-sm
               hover:bg-primary-yellow dark:hover:bg-primary-yellow active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
        :title="isDark ? '切换亮色模式' : '切换暗色模式'"
      >
        <!-- Sun icon (shown in dark mode) -->
        <svg v-if="isDark" class="w-5 h-5 text-primary-yellow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
        </svg>
        <!-- Moon icon (shown in light mode) -->
        <svg v-else class="w-5 h-5 text-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
        </svg>
      </button>

      <div class="relative">
        <button
          @click="toggleFolders"
          class="px-4 py-2 text-sm font-bold uppercase tracking-wider border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface shadow-hard-sm dark:shadow-dark-hard-sm
                 hover:bg-muted dark:hover:bg-dark-muted active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200 flex items-center gap-2
                 text-foreground dark:text-dark-text-main"
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
        class="px-4 py-2 text-sm font-bold uppercase tracking-wider bg-primary-red text-white border-2 border-foreground dark:border-dark-border shadow-hard-sm dark:shadow-dark-hard-sm
               hover:bg-primary-red/90 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200 flex items-center gap-2"
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
