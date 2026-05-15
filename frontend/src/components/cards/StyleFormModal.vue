<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Style, StyleCreateInput, StyleUpdateInput, ITuneTrack } from '@/types'
import { useStylesStore } from '@/stores/styles'
import { useGenresStore } from '@/stores/genres'
import { useITuneSearch } from '@/composables/useITuneSearch'
import { useAudio } from '@/composables/useAudio'

const props = defineProps<{
  style?: Style
}>()

const emit = defineEmits<{
  close: []
}>()

const stylesStore = useStylesStore()
const genresStore = useGenresStore()
const { tracks: itunesTracks, loading: itunesLoading, search: itunesSearch, trackToMetadata, clear: clearITunes } = useITuneSearch()
const { play, isCurrentlyPlaying, stop } = useAudio()

const isEdit = computed(() => !!props.style)
const title = computed(() => isEdit.value ? '编辑风格' : '添加新风格')

const form = ref({
  name: '',
  tags: '',
  genre_id: '' as string | null,
  description: '',
  bpm_range: '',
  audio_type: '' as 'local' | 'url' | '',
  audio_source: '',
  audio_platform: '' as 'local' | 'url' | 'itunes' | '',
  audio_metadata: '',
  reference_url: '',
})

const loading = ref(false)
const error = ref<string | null>(null)

// iTunes search state
const itunesQuery = ref('')
const showITunesPanel = ref(false)
const itunesPreviewId = ref<string | null>(null)
let searchDebounce: ReturnType<typeof setTimeout> | null = null

onMounted(() => {
  if (props.style) {
    form.value = {
      name: props.style.name,
      tags: props.style.tags.join(', '),
      genre_id: props.style.genre_id,
      description: props.style.description || '',
      bpm_range: props.style.bpm_range || '',
      audio_type: props.style.audio_type || '',
      audio_source: props.style.audio_source || '',
      audio_platform: props.style.audio_platform || '',
      audio_metadata: props.style.audio_metadata || '',
      reference_url: props.style.reference_url || '',
    }
  }
})

// Watch genre selection to provide genre hint for iTunes search
const selectedGenreName = computed(() => {
  if (!form.value.genre_id) return undefined
  function findGenreName(genres: typeof genresStore.genres, id: string): string | undefined {
    for (const g of genres) {
      if (g.id === id) return g.name
      if (g.children?.length) {
        const found = findGenreName(g.children, id)
        if (found) return found
      }
    }
    return undefined
  }
  return findGenreName(genresStore.genres, form.value.genre_id)
})

function flattenGenres(genres: typeof genresStore.genres, prefix = ''): Array<{ id: string; label: string }> {
  const result: Array<{ id: string; label: string }> = []
  for (const genre of genres) {
    result.push({ id: genre.id, label: prefix + genre.name })
    if (genre.children?.length) {
      result.push(...flattenGenres(genre.children, prefix + '  '))
    }
  }
  return result
}

const genreOptions = computed(() => flattenGenres(genresStore.genres))

// iTunes search with debounce
function onITunesInput() {
  if (searchDebounce) clearTimeout(searchDebounce)
  if (!itunesQuery.value.trim()) {
    clearITunes()
    return
  }
  searchDebounce = setTimeout(() => {
    itunesSearch(itunesQuery.value, selectedGenreName.value)
  }, 400)
}

function selectITuneTrack(track: ITuneTrack) {
  const previewUrl = track.preview_url || ''
  form.value.audio_type = 'url'
  form.value.audio_source = previewUrl
  form.value.audio_platform = 'itunes'
  form.value.audio_metadata = trackToMetadata(track)
  showITunesPanel.value = false
  itunesPreviewId.value = null
  stop()
}

function previewITuneTrack(track: ITuneTrack) {
  if (!track.preview_url) return
  const id = `itunes-${track.track_id}`
  if (itunesPreviewId.value === id && isCurrentlyPlaying(id)) {
    stop()
    itunesPreviewId.value = null
  } else {
    play(id, track.preview_url)
    itunesPreviewId.value = id
  }
}

function isTrackPlaying(track: ITuneTrack): boolean {
  return isCurrentlyPlaying(`itunes-${track.track_id}`)
}

function toggleITunesPanel() {
  showITunesPanel.value = !showITunesPanel.value
  if (!showITunesPanel.value) {
    clearITunes()
    itunesQuery.value = ''
    stop()
  }
}

// Get current audio display info
const audioDisplayInfo = computed(() => {
  if (!form.value.audio_metadata) return null
  try {
    return JSON.parse(form.value.audio_metadata)
  } catch {
    return null
  }
})

function clearAudioSelection() {
  form.value.audio_type = ''
  form.value.audio_source = ''
  form.value.audio_platform = ''
  form.value.audio_metadata = ''
  stop()
}

async function handleSubmit() {
  if (!form.value.name.trim() || !form.value.tags.trim()) {
    error.value = '名称和标签为必填项'
    return
  }

  loading.value = true
  error.value = null

  const tagsArray = form.value.tags.split(/[,，]/).map(t => t.trim()).filter(Boolean)
  
  try {
    if (isEdit.value && props.style) {
      const updateData: StyleUpdateInput = {
        name: form.value.name,
        tags: tagsArray,
        genre_id: form.value.genre_id || null,
        description: form.value.description || null,
        bpm_range: form.value.bpm_range || null,
        audio_type: (form.value.audio_type as 'local' | 'url') || null,
        audio_source: form.value.audio_source || null,
        audio_platform: (form.value.audio_platform as 'local' | 'url' | 'itunes') || null,
        audio_metadata: form.value.audio_metadata || null,
        reference_url: form.value.reference_url || null,
      }
      await stylesStore.editStyle(props.style.id, updateData)
    } else {
      const createData: StyleCreateInput = {
        name: form.value.name,
        tags: tagsArray,
        genre_id: form.value.genre_id || null,
        description: form.value.description || null,
        bpm_range: form.value.bpm_range || null,
        audio_type: (form.value.audio_type as 'local' | 'url') || null,
        audio_source: form.value.audio_source || null,
        audio_platform: (form.value.audio_platform as 'local' | 'url' | 'itunes') || null,
        audio_metadata: form.value.audio_metadata || null,
        reference_url: form.value.reference_url || null,
      }
      await stylesStore.addStyle(createData)
    }
    emit('close')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '操作失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto py-8">
      <div class="absolute inset-0 bg-void/80" @click="emit('close')"></div>
      
      <!-- Terminal-style modal -->
      <div class="relative border-2 border-neon-cyan bg-black/80 shadow-neon-cyan-lg w-full max-w-lg mx-4 max-h-[90vh] flex flex-col">
        <!-- Title bar with window chrome -->
        <div class="flex items-center justify-between bg-neon-cyan/10 border-b border-neon-cyan px-4 py-2 flex-shrink-0">
          <div class="flex items-center gap-2">
            <div class="h-3 w-3 rounded-full bg-neon-magenta"></div>
            <div class="h-3 w-3 rounded-full bg-neon-cyan"></div>
            <div class="h-3 w-3 rounded-full bg-neon-orange"></div>
          </div>
          <span class="font-mono text-xs text-neon-cyan/60">{{ isEdit ? 'edit_style.exe' : 'new_style.exe' }}</span>
          <button @click="emit('close')" class="text-text-sub hover:text-neon-magenta transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="p-6 overflow-y-auto">
          <h2 class="font-heading font-bold text-2xl uppercase tracking-wider text-neon-cyan glow-text-cyan mb-6">{{ title }}</h2>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 风格名称 *</label>
              <input
                v-model="form.name"
                type="text"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
                placeholder="如 Synthwave"
              />
            </div>

            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 风格标签 * (逗号分隔)</label>
              <input
                v-model="form.tags"
                type="text"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
                placeholder="retrowave, analog synth, 80s"
              />
            </div>

            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 所属流派</label>
              <select
                v-model="form.genre_id"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
              >
                <option value="">-- 选择流派 --</option>
                <option v-for="opt in genreOptions" :key="opt.id" :value="opt.id">
                  {{ opt.label }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 风格描述</label>
              <textarea
                v-model="form.description"
                rows="2"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors resize-none"
                placeholder="对这个风格的简要描述"
              ></textarea>
            </div>

            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> BPM 范围</label>
              <input
                v-model="form.bpm_range"
                type="text"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
                placeholder="100-120"
              />
            </div>

            <!-- ===== 示例音频区 ===== -->
            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 示例音频</label>

              <!-- Current selection display -->
              <div v-if="form.audio_source" class="mb-3 flex items-center gap-2 px-3 py-2 border border-neon-cyan/30 bg-neon-cyan/5">
                <div v-if="audioDisplayInfo?.artwork_url" class="w-10 h-10 flex-shrink-0 overflow-hidden">
                  <img :src="audioDisplayInfo.artwork_url" :alt="audioDisplayInfo.track_name" class="w-full h-full object-cover" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm text-neon-cyan font-mono truncate">{{ audioDisplayInfo?.track_name || '音频文件' }}</div>
                  <div v-if="audioDisplayInfo?.artist_name" class="text-xs text-chrome/60 font-mono truncate">{{ audioDisplayInfo.artist_name }}</div>
                  <div v-if="form.audio_platform === 'itunes'" class="text-[10px] text-neon-orange/70 font-mono mt-0.5">iTunes 30s Preview</div>
                </div>
                <button @click="clearAudioSelection()" class="p-1 text-text-sub hover:text-neon-magenta transition" title="移除">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>

              <!-- Audio source tabs -->
              <div v-if="!form.audio_source" class="space-y-3">
                <!-- iTunes search button -->
                <button
                  type="button"
                  @click="toggleITunesPanel"
                  class="w-full py-2.5 border-2 border-neon-cyan/50 text-sm font-mono uppercase tracking-wider text-neon-cyan
                         hover:bg-neon-cyan hover:text-void hover:shadow-neon-cyan hover:border-neon-cyan
                         transition-all duration-200 flex items-center justify-center gap-2"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                  </svg>
                  从 iTunes 搜索试听片段
                </button>

                <!-- Manual URL / Local input -->
                <div class="flex gap-4 mb-2">
                  <label class="flex items-center gap-2 cursor-pointer font-mono text-chrome text-sm">
                    <input type="radio" v-model="form.audio_type" value="url" class="accent-neon-magenta" />
                    外部链接
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer font-mono text-chrome text-sm">
                    <input type="radio" v-model="form.audio_type" value="local" class="accent-neon-magenta" />
                    本地文件
                  </label>
                </div>
                <input
                  v-if="form.audio_type === 'url' || form.audio_type === 'local'"
                  v-model="form.audio_source"
                  type="text"
                  class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                         placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
                  :placeholder="form.audio_type === 'local' ? '/storage/audio/xxx.mp3' : 'https://example.com/audio.mp3'"
                />
              </div>
            </div>

            <!-- ===== iTunes Search Panel ===== -->
            <div v-if="showITunesPanel" class="border-2 border-neon-cyan/40 bg-black/50 p-3 space-y-3">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-mono text-neon-cyan/70 uppercase tracking-wider">iTunes Search</span>
                <button @click="toggleITunesPanel()" class="text-text-sub hover:text-neon-magenta transition p-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>

              <input
                v-model="itunesQuery"
                type="text"
                @input="onITunesInput()"
                class="w-full border-b-2 border-neon-cyan bg-black text-neon-cyan font-mono text-sm px-1 py-2
                       placeholder:text-neon-cyan/30 focus:outline-none transition-colors"
                placeholder="搜索歌曲或艺术家... (如: Daft Punk)"
              />

              <div v-if="selectedGenreName" class="text-[10px] font-mono text-neon-orange/70">
                Genre hint: {{ selectedGenreName }}
              </div>

              <!-- Loading -->
              <div v-if="itunesLoading" class="text-center py-4">
                <div class="inline-block animate-spin w-5 h-5 border-2 border-neon-cyan border-t-transparent rounded-full"></div>
              </div>

              <!-- Results -->
              <div v-else-if="itunesTracks.length" class="space-y-1 max-h-52 overflow-y-auto">
                <div
                  v-for="track in itunesTracks"
                  :key="track.track_id"
                  class="flex items-center gap-2 px-2 py-1.5 hover:bg-neon-cyan/10 cursor-pointer group transition-colors"
                  @click="selectITuneTrack(track)"
                >
                  <!-- Artwork -->
                  <div class="w-9 h-9 flex-shrink-0 bg-panel overflow-hidden">
                    <img v-if="track.artwork_url100" :src="track.artwork_url100" class="w-full h-full object-cover" />
                  </div>

                  <!-- Track info -->
                  <div class="flex-1 min-w-0">
                    <div class="text-sm text-chrome font-mono truncate group-hover:text-neon-cyan transition-colors">{{ track.track_name }}</div>
                    <div class="text-xs text-text-sub font-mono truncate">{{ track.artist_name }}</div>
                  </div>

                  <!-- Genre badge -->
                  <span v-if="track.primary_genre_name" class="text-[9px] font-mono px-1 py-0.5 bg-neon-magenta/10 text-neon-magenta/70 border border-neon-magenta/20 flex-shrink-0">
                    {{ track.primary_genre_name }}
                  </span>

                  <!-- Preview button -->
                  <button
                    v-if="track.preview_url"
                    @click.stop="previewITuneTrack(track)"
                    class="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-200 border"
                    :class="isTrackPlaying(track) 
                      ? 'bg-neon-magenta border-neon-magenta text-white animate-pulse-glow' 
                      : 'border-neon-cyan/40 text-neon-cyan/60 hover:border-neon-cyan hover:text-neon-cyan'"
                  >
                    <svg v-if="isTrackPlaying(track)" class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
                    </svg>
                    <svg v-else class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- No results -->
              <div v-else-if="itunesQuery && !itunesLoading" class="text-center py-3 text-xs font-mono text-text-sub">
                未找到结果，尝试其他关键词
              </div>
            </div>

            <div>
              <label class="block text-xs font-mono uppercase tracking-widest text-neon-magenta mb-1">> 参考来源 URL</label>
              <input
                v-model="form.reference_url"
                type="text"
                class="w-full border-b-2 border-neon-magenta bg-black text-neon-cyan font-mono text-lg px-1 py-2
                       placeholder:text-neon-magenta/40 focus:border-neon-cyan focus:shadow-neon-cyan focus:outline-none transition-colors"
                placeholder="https://everynoise.com/..."
              />
            </div>

            <div v-if="error" class="text-neon-magenta text-sm font-mono glow-text-magenta">ERROR: {{ error }}</div>

            <div class="flex justify-end gap-3 pt-4">
              <button
                type="button"
                @click="emit('close')"
                class="-skew-x-12 border-2 border-neon-cyan bg-transparent text-neon-cyan font-mono uppercase tracking-wider text-sm px-4 py-2
                       hover:skew-x-0 hover:bg-neon-cyan hover:text-void hover:shadow-neon-cyan transition-all duration-200"
              >
                <span class="inline-block skew-x-12">取消</span>
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="-skew-x-12 border-2 border-neon-magenta bg-neon-magenta text-white font-mono uppercase tracking-wider text-sm px-4 py-2
                       hover:skew-x-0 hover:scale-105 hover:shadow-neon-magenta-lg
                       disabled:opacity-50 transition-all duration-200"
              >
                <span class="inline-block skew-x-12">{{ loading ? '保存中...' : '保存' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Teleport>
</template>
