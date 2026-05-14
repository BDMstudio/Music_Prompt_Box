<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppSidebar from './components/layout/AppSidebar.vue'
import AppMain from './components/layout/AppMain.vue'
import Toast from './components/common/Toast.vue'
import { useGenresStore } from './stores/genres'
import { useStylesStore } from './stores/styles'
import { useFoldersStore } from './stores/folders'
import { useTagsStore } from './stores/tags'

const genresStore = useGenresStore()
const stylesStore = useStylesStore()
const foldersStore = useFoldersStore()
const tagsStore = useTagsStore()

onMounted(async () => {
  await Promise.all([
    genresStore.loadGenres(),
    stylesStore.loadStyles(),
    foldersStore.loadFolders(),
    tagsStore.loadHotTags(),
  ])
})
</script>

<template>
  <div class="h-screen flex flex-col bg-void text-chrome relative overflow-hidden">
    <!-- CRT scanlines overlay -->
    <div class="crt-scanlines fixed inset-0 z-50 pointer-events-none"></div>

    <!-- Floating sun — centered to avoid right overflow -->
    <div class="fixed top-[-200px] left-1/2 -translate-x-1/2 h-[600px] w-[600px] blur-[100px] bg-gradient-to-b from-neon-orange to-neon-magenta opacity-15 pointer-events-none z-0"></div>

    <!-- Content -->
    <div class="relative z-10 flex flex-col h-full">
      <AppHeader />
      <div class="flex flex-1 overflow-hidden">
        <!-- Sidebar: hidden on mobile, visible on md+ -->
        <div class="hidden md:flex flex-shrink-0 h-full overflow-hidden">
          <AppSidebar />
        </div>
        <AppMain />
      </div>
      <Toast />
    </div>
  </div>
</template>
