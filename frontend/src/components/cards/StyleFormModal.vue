<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Style, StyleCreateInput, StyleUpdateInput } from '@/types'
import { useStylesStore } from '@/stores/styles'
import { useGenresStore } from '@/stores/genres'

const props = defineProps<{
  style?: Style
}>()

const emit = defineEmits<{
  close: []
}>()

const stylesStore = useStylesStore()
const genresStore = useGenresStore()

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
  reference_url: '',
})

const loading = ref(false)
const error = ref<string | null>(null)

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
      reference_url: props.style.reference_url || '',
    }
  }
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
      <div class="absolute inset-0 bg-foreground/60 dark:bg-black/70" @click="emit('close')"></div>
      
      <div class="relative bg-white dark:bg-dark-surface border-4 border-foreground dark:border-dark-border p-6 w-full max-w-lg shadow-hard-lg dark:shadow-dark-hard-lg mx-4 transition-colors duration-300">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6 border-b-4 border-foreground dark:border-dark-border pb-4">
          <h2 class="text-2xl font-black uppercase tracking-tighter text-foreground dark:text-dark-text-main">{{ title }}</h2>
          <button @click="emit('close')" class="p-1 text-foreground dark:text-dark-text-main hover:bg-primary-red hover:text-white transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">风格名称 *</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
              placeholder="如 Synthwave"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">风格标签 * (逗号分隔)</label>
            <input
              v-model="form.tags"
              type="text"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
              placeholder="retrowave, analog synth, 80s"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">所属流派</label>
            <select
              v-model="form.genre_id"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
            >
              <option value="">-- 选择流派 --</option>
              <option v-for="opt in genreOptions" :key="opt.id" :value="opt.id">
                {{ opt.label }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">风格描述</label>
            <textarea
              v-model="form.description"
              rows="2"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red resize-none transition-colors"
              placeholder="对这个风格的简要描述"
            ></textarea>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">BPM 范围</label>
            <input
              v-model="form.bpm_range"
              type="text"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
              placeholder="100-120"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">示例音频</label>
            <div class="flex gap-4 mb-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="form.audio_type" value="url" class="accent-primary-red" />
                <span class="text-sm font-medium text-foreground dark:text-dark-text-main">外部链接</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="form.audio_type" value="local" class="accent-primary-red" />
                <span class="text-sm font-medium text-foreground dark:text-dark-text-main">本地文件</span>
              </label>
            </div>
            <input
              v-model="form.audio_source"
              type="text"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
              :placeholder="form.audio_type === 'local' ? '/storage/audio/xxx.mp3' : 'https://example.com/audio.mp3'"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-foreground dark:text-dark-text-main mb-1">参考来源 URL</label>
            <input
              v-model="form.reference_url"
              type="text"
              class="w-full px-3 py-2 bg-background dark:bg-dark-surface-alt border-2 border-foreground dark:border-dark-border text-foreground dark:text-dark-text-main font-medium focus:outline-none focus:border-primary-red transition-colors"
              placeholder="https://everynoise.com/..."
            />
          </div>

          <div v-if="error" class="text-primary-red text-sm font-bold">{{ error }}</div>

          <div class="flex justify-end gap-3 pt-4">
            <button
              type="button"
              @click="emit('close')"
              class="px-4 py-2 text-sm font-bold uppercase tracking-wider border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface shadow-hard-sm dark:shadow-dark-hard-sm
                     text-foreground dark:text-dark-text-main
                     hover:bg-muted dark:hover:bg-dark-muted active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="px-4 py-2 text-sm font-bold uppercase tracking-wider bg-primary-blue text-white border-2 border-foreground dark:border-dark-border shadow-hard-sm dark:shadow-dark-hard-sm
                     hover:bg-primary-blue/90 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200
                     disabled:opacity-50"
            >
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
