<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Genre } from '@/types'
import { useGenresStore } from '@/stores/genres'
import { useClipboard } from '@/composables/useClipboard'

const props = defineProps<{
  genre: Genre
}>()

const expanded = ref(true)
const genresStore = useGenresStore()
const { copy } = useClipboard()

const hasChildren = computed(() => props.genre.children && props.genre.children.length > 0)
const isSelected = computed(() => genresStore.selectedGenreId === props.genre.id)

function toggleExpand() {
  if (hasChildren.value) {
    expanded.value = !expanded.value
  }
}

function selectGenre() {
  genresStore.selectGenre(props.genre.id)
}

function copyEraPrompt() {
  if (props.genre.era_prompt) {
    copy(props.genre.era_prompt, '时代提示词已复制')
  }
}
</script>

<template>
  <div class="relative">
    <div
      class="relative pl-4 py-2 pr-2 rounded-lg cursor-pointer transition-all group"
      :class="isSelected ? 'bg-accent/20' : 'hover:bg-zinc-800/50'"
    >
      <div class="absolute left-[-6px] top-4 w-3 h-3 rounded-full border-2 transition-all"
        :class="isSelected 
          ? 'bg-accent border-white shadow-[0_0_10px_rgba(139,92,246,0.5)]' 
          : 'bg-card-bg border-zinc-600 group-hover:border-accent'"
      ></div>

      <div class="flex items-center gap-2">
        <button
          v-if="hasChildren"
          @click.stop="toggleExpand"
          class="w-4 h-4 flex items-center justify-center text-zinc-500 hover:text-white"
        >
          <svg
            class="w-3 h-3 transition-transform"
            :class="expanded ? 'rotate-90' : ''"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
        <div v-else class="w-4"></div>

        <div class="flex-1 min-w-0" @click="selectGenre">
          <div class="flex items-center gap-2">
            <span
              class="font-bold text-lg"
              :class="isSelected ? 'text-white' : 'text-zinc-300'"
            >
              {{ genre.name }}
            </span>
            <button
              v-if="genre.era_prompt"
              @click.stop="copyEraPrompt"
              class="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-accent/30 transition"
              title="复制时代提示词"
            >
              <svg class="w-3 h-3 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
          <p v-if="genre.description" class="text-xs text-text-sub truncate mt-0.5">
            {{ genre.description }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="hasChildren && expanded" class="ml-4 mt-1">
      <GenreNode v-for="child in genre.children" :key="child.id" :genre="child" />
    </div>
  </div>
</template>
