<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Style } from '@/types'
import TagPill from '../tags/TagPill.vue'
import StyleFormModal from './StyleFormModal.vue'
import ConfirmModal from '../common/ConfirmModal.vue'
import { useAudio } from '@/composables/useAudio'
import { useClipboard } from '@/composables/useClipboard'
import { useStylesStore } from '@/stores/styles'
import { useTagsStore } from '@/stores/tags'
import { useFoldersStore } from '@/stores/folders'

const props = defineProps<{
  style: Style
}>()

const stylesStore = useStylesStore()
const tagsStore = useTagsStore()
const foldersStore = useFoldersStore()
const { play, isCurrentlyPlaying } = useAudio()
const { copy } = useClipboard()

const showEditModal = ref(false)
const showDeleteConfirm = ref(false)
const showFolderMenu = ref(false)

const isPlaying = computed(() => isCurrentlyPlaying(props.style.id))
const hasAudio = computed(() => !!props.style.audio_source)

function togglePlay() {
  if (hasAudio.value && props.style.audio_source) {
    play(props.style.id, props.style.audio_source)
  }
}

async function copyAllTags() {
  const allTags = props.style.tags.join(' ')
  await copy(allTags, '全部标签已复制')
  tagsStore.recordCopies(props.style.tags)
  stylesStore.recordCopy(props.style.id)
}

async function handleDelete() {
  await stylesStore.removeStyle(props.style.id)
  showDeleteConfirm.value = false
}

async function addToFolder(folderId: string) {
  await foldersStore.addToFolder(folderId, props.style.id)
  showFolderMenu.value = false
  await stylesStore.loadStyles()
}
</script>

<template>
  <div class="border border-neon-magenta/30 border-t-2 border-t-neon-cyan bg-panel backdrop-blur-md p-5
              hover:-translate-y-2 hover:shadow-neon-cyan transition-all duration-200 group">
    <!-- Top row: genre badge + actions -->
    <div class="flex items-start justify-between mb-3">
      <span class="text-xs font-mono px-2 py-0.5 bg-neon-magenta/10 text-neon-magenta border border-neon-magenta/30 uppercase tracking-wider">
        {{ style.genre_name || 'Unknown' }}
      </span>
      
      <div class="flex items-center gap-1">
        <!-- Folder button -->
        <div class="relative">
          <button
            @click="showFolderMenu = !showFolderMenu"
            class="p-1.5 opacity-0 group-hover:opacity-100 hover:bg-neon-magenta/20 transition"
            :class="style.is_favorited ? 'text-neon-orange opacity-100' : 'text-text-sub'"
            title="添加到收藏夹"
          >
            <svg class="w-4 h-4" :fill="style.is_favorited ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>

          <div
            v-if="showFolderMenu"
            class="absolute right-0 top-full mt-1 w-44 bg-panel-solid border-2 border-neon-cyan shadow-neon-cyan z-10 py-1"
          >
            <div
              v-for="folder in foldersStore.folders"
              :key="folder.id"
              @click="addToFolder(folder.id)"
              class="px-3 py-2 text-sm font-mono text-chrome hover:bg-neon-cyan/10 cursor-pointer"
            >
              {{ folder.name }}
            </div>
            <div v-if="foldersStore.folders.length === 0" class="px-3 py-2 text-sm text-text-sub font-mono">
              暂无收藏夹
            </div>
          </div>
        </div>

        <!-- Edit button -->
        <button
          @click="showEditModal = true"
          class="p-1.5 text-text-sub opacity-0 group-hover:opacity-100 hover:bg-neon-cyan/20 hover:text-neon-cyan transition"
          title="编辑"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>

        <!-- Delete button -->
        <button
          @click="showDeleteConfirm = true"
          class="p-1.5 text-text-sub opacity-0 group-hover:opacity-100 hover:bg-neon-magenta/30 hover:text-neon-magenta transition"
          title="删除"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Title + audio play -->
    <div class="flex items-center gap-3 mb-3">
      <h3 class="font-heading font-semibold text-2xl text-neon-cyan glow-text-cyan flex-1">{{ style.name }}</h3>
      
      <button
        v-if="hasAudio"
        @click="togglePlay"
        class="w-9 h-9 rounded-full flex items-center justify-center transition-all duration-200 flex-shrink-0 border-2"
        :class="isPlaying ? 'bg-neon-magenta border-neon-magenta text-white animate-pulse-glow' : 'bg-transparent border-neon-cyan text-neon-cyan hover:bg-neon-cyan hover:text-void'"
      >
        <svg v-if="isPlaying" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
        </svg>
        <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
    </div>

    <!-- Tags -->
    <div class="flex flex-wrap gap-1.5 mb-4">
      <TagPill v-for="tag in style.tags" :key="tag" :tag="tag" />
    </div>

    <!-- Description -->
    <p v-if="style.description" class="text-sm text-chrome/70 mb-4 line-clamp-2 font-mono">
      {{ style.description }}
    </p>

    <!-- BPM -->
    <div v-if="style.bpm_range" class="text-xs text-neon-orange/70 mb-4 font-mono uppercase tracking-wider">
      > BPM: {{ style.bpm_range }}
    </div>

    <!-- Copy all tags button -->
    <button
      @click="copyAllTags"
      class="w-full py-2 border-2 border-neon-magenta/50 text-sm font-mono uppercase tracking-wider text-neon-magenta
             hover:bg-neon-magenta hover:text-white hover:shadow-neon-magenta hover:border-neon-magenta
             transition-all duration-200 flex items-center justify-center gap-2"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
      </svg>
      复制全部标签
    </button>
  </div>

  <StyleFormModal
    v-if="showEditModal"
    :style="style"
    @close="showEditModal = false"
  />

  <ConfirmModal
    v-if="showDeleteConfirm"
    title="确认删除"
    :message="`确定要删除「${style.name}」吗？此操作无法撤销。`"
    confirm-text="删除"
    @confirm="handleDelete"
    @cancel="showDeleteConfirm = false"
  />
</template>
