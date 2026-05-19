<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import FolderList from '../folders/FolderList.vue'
import StyleFormModal from '../cards/StyleFormModal.vue'
import { useAudio } from '@/composables/useAudio'

const { isPlaying } = useAudio()

const showFolders = ref(false)
const showAddModal = ref(false)

// ── Dot bounce animation ──
type BounceMode = 'idle' | 'playing' | 'none'
const bounceMode = ref<BounceMode>('none')

let idleTimer: ReturnType<typeof setInterval> | null = null
let idleResetTimer: ReturnType<typeof setTimeout> | null = null

function triggerIdleBounce() {
  // Don't interrupt playing animation
  if (bounceMode.value === 'playing') return
  bounceMode.value = 'idle'
  if (idleResetTimer) clearTimeout(idleResetTimer)
  idleResetTimer = setTimeout(() => {
    if (bounceMode.value === 'idle') bounceMode.value = 'none'
  }, 3000)
}

// Watch audio: toggle bounce with forced restart via nextTick
watch(isPlaying, async (playing) => {
  if (playing) {
    // Force restart: clear animation first, then set in next frame
    bounceMode.value = 'none'
    await nextTick()
    bounceMode.value = 'playing'
  } else if (bounceMode.value === 'playing') {
    bounceMode.value = 'none'
  }
})

onMounted(() => {
  idleTimer = setInterval(triggerIdleBounce, 60_000)
  // First idle bounce after 5s so user sees it quickly
  setTimeout(triggerIdleBounce, 5_000)
})

onUnmounted(() => {
  if (idleTimer) clearInterval(idleTimer)
  if (idleResetTimer) clearTimeout(idleResetTimer)
})

function toggleFolders() {
  showFolders.value = !showFolders.value
}

function openAddModal() {
  showAddModal.value = true
}
</script>

<template>
  <header class="h-[60px] flex-shrink-0 bg-void/90 backdrop-blur-md border-b-2 border-border-dim flex items-center justify-between px-4 md:px-4">
    <!-- Logo -->
    <div class="flex items-center gap-2 md:gap-3 min-w-0">
      <div class="flex items-center gap-1.5 flex-shrink-0">
        <div
          v-if="bounceMode === 'playing'"
          class="w-3 h-3 rounded-full bg-neon-magenta animate-bounce1-loop"
        ></div>
        <div
          v-else-if="bounceMode === 'idle'"
          class="w-3 h-3 rounded-full bg-neon-magenta animate-bounce1-once"
        ></div>
        <div v-else class="w-3 h-3 rounded-full bg-neon-magenta"></div>

        <div
          v-if="bounceMode === 'playing'"
          class="w-3 h-3 rounded-full bg-neon-cyan animate-bounce2-loop"
        ></div>
        <div
          v-else-if="bounceMode === 'idle'"
          class="w-3 h-3 rounded-full bg-neon-cyan animate-bounce2-once"
        ></div>
        <div v-else class="w-3 h-3 rounded-full bg-neon-cyan"></div>

        <div
          v-if="bounceMode === 'playing'"
          class="w-3 h-3 rounded-full bg-neon-orange animate-bounce3-loop"
        ></div>
        <div
          v-else-if="bounceMode === 'idle'"
          class="w-3 h-3 rounded-full bg-neon-orange animate-bounce3-once"
        ></div>
        <div v-else class="w-3 h-3 rounded-full bg-neon-orange"></div>
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

<style scoped>
/*
  Bounce keyframes — spring-like feel with 2 rebounds per bounce.
  3 balls fire sequentially within a 3s cycle.
  Amplitude decreases: ball1(-8px) → ball2(-6px) → ball3(-4px)
  Each ball: rise → fall → rebound → fall → micro-rebound → settle
*/

@keyframes bounce1 {
  0%    { transform: translateY(0); }
  4%    { transform: translateY(-8px); }
  9%    { transform: translateY(0); }
  12%   { transform: translateY(-3px); }
  15%   { transform: translateY(0); }
  17%   { transform: translateY(-1px); }
  19%   { transform: translateY(0); }
  100%  { transform: translateY(0); }
}

@keyframes bounce2 {
  0%    { transform: translateY(0); }
  33%   { transform: translateY(0); }
  37%   { transform: translateY(-6px); }
  42%   { transform: translateY(0); }
  45%   { transform: translateY(-2px); }
  48%   { transform: translateY(0); }
  50%   { transform: translateY(-0.5px); }
  52%   { transform: translateY(0); }
  100%  { transform: translateY(0); }
}

@keyframes bounce3 {
  0%    { transform: translateY(0); }
  65%   { transform: translateY(0); }
  69%   { transform: translateY(-4px); }
  74%   { transform: translateY(0); }
  77%   { transform: translateY(-1.5px); }
  80%   { transform: translateY(0); }
  82%   { transform: translateY(-0.5px); }
  84%   { transform: translateY(0); }
  100%  { transform: translateY(0); }
}

/* Idle: single 3s cycle */
.animate-bounce1-once { animation: bounce1 3s linear; }
.animate-bounce2-once { animation: bounce2 3s linear; }
.animate-bounce3-once { animation: bounce3 3s linear; }

/* Playing: infinite loop */
.animate-bounce1-loop { animation: bounce1 3s linear infinite; }
.animate-bounce2-loop { animation: bounce2 3s linear infinite; }
.animate-bounce3-loop { animation: bounce3 3s linear infinite; }
</style>
