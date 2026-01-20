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
  <div class="h-screen flex flex-col bg-app-bg">
    <AppHeader />
    <div class="flex flex-1 overflow-hidden">
      <AppSidebar />
      <AppMain />
    </div>
    <Toast />
  </div>
</template>
