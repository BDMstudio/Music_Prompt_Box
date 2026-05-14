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
      class="relative py-2 pr-2 cursor-pointer transition-all duration-200 group border border-transparent"
      :class="isSelected ? 'border-neon-cyan/30 bg-neon-cyan/5' : 'hover:bg-neon-magenta/5'"
    >
      <div class="flex items-center gap-2">
        <button
          v-if="hasChildren"
          @click.stop="toggleExpand"
          class="w-4 h-4 flex items-center justify-center text-text-sub hover:text-neon-cyan"
        >
          <svg
            class="w-3 h-3 transition-transform duration-200"
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
              class="font-mono font-bold text-sm uppercase tracking-wider"
              :class="isSelected ? 'text-neon-cyan glow-text-cyan' : 'text-chrome'"
            >
              {{ genre.name }}
            </span>
            <button
              v-if="genre.era_prompt"
              @click.stop="copyEraPrompt"
              class="opacity-0 group-hover:opacity-100 p-1 hover:bg-neon-magenta/20 transition"
              title="复制时代提示词"
            >
              <svg class="w-3 h-3 text-neon-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
          <p v-if="genre.description" class="text-xs text-text-sub truncate mt-0.5 font-mono">
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
