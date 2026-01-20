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
  <div class="bg-card-bg border border-border rounded-2xl p-5 hover:border-zinc-600 hover:shadow-xl hover:-translate-y-1 transition-all group">
    <div class="flex items-start justify-between mb-3">
      <span class="text-xs font-bold px-2 py-0.5 bg-zinc-800 text-zinc-500 rounded uppercase">
        {{ style.genre_name || 'Unknown' }}
      </span>
      
      <div class="flex items-center gap-1">
        <div class="relative">
          <button
            @click="showFolderMenu = !showFolderMenu"
            class="p-1.5 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-zinc-700 transition"
            :class="style.is_favorited ? 'text-yellow-500 opacity-100' : 'text-zinc-500'"
            title="添加到收藏夹"
          >
            <svg class="w-4 h-4" :fill="style.is_favorited ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>

          <div
            v-if="showFolderMenu"
            class="absolute right-0 top-full mt-1 w-40 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl z-10 py-1"
          >
            <div
              v-for="folder in foldersStore.folders"
              :key="folder.id"
              @click="addToFolder(folder.id)"
              class="px-3 py-2 text-sm hover:bg-zinc-800 cursor-pointer"
            >
              {{ folder.name }}
            </div>
            <div v-if="foldersStore.folders.length === 0" class="px-3 py-2 text-sm text-zinc-500">
              暂无收藏夹
            </div>
          </div>
        </div>

        <button
          @click="showEditModal = true"
          class="p-1.5 rounded-lg text-zinc-500 opacity-0 group-hover:opacity-100 hover:bg-zinc-700 hover:text-white transition"
          title="编辑"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>

        <button
          @click="showDeleteConfirm = true"
          class="p-1.5 rounded-lg text-zinc-500 opacity-0 group-hover:opacity-100 hover:bg-red-900/50 hover:text-red-400 transition"
          title="删除"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="flex items-center gap-3 mb-3">
      <h3 class="text-lg font-bold text-white flex-1">{{ style.name }}</h3>
      
      <button
        v-if="hasAudio"
        @click="togglePlay"
        class="w-9 h-9 rounded-full flex items-center justify-center transition flex-shrink-0"
        :class="isPlaying ? 'bg-accent animate-pulse-glow' : 'bg-zinc-700 hover:bg-white hover:text-black'"
      >
        <svg v-if="isPlaying" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
        </svg>
        <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
    </div>

    <div class="flex flex-wrap gap-1.5 mb-4">
      <TagPill v-for="tag in style.tags" :key="tag" :tag="tag" />
    </div>

    <p v-if="style.description" class="text-sm text-text-sub mb-4 line-clamp-2">
      {{ style.description }}
    </p>

    <div v-if="style.bpm_range" class="text-xs text-zinc-600 mb-4">
      BPM: {{ style.bpm_range }}
    </div>

    <button
      @click="copyAllTags"
      class="w-full py-2 border border-dashed border-zinc-600 rounded-lg text-sm text-zinc-400 hover:border-white hover:text-white hover:bg-zinc-800/50 transition flex items-center justify-center gap-2"
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
