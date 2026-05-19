<script setup lang="ts">
import { computed } from 'vue'
import { useAudio } from '@/composables/useAudio'

const { isPlaying, currentStyle, currentTime, duration, stop, seek } = useAudio()

const show = computed(() => isPlaying.value && currentStyle.value)

// Parse artwork from audio_metadata
const artwork = computed(() => {
  if (!currentStyle.value?.audio_metadata) return null
  try {
    const meta = JSON.parse(currentStyle.value.audio_metadata)
    return meta.artwork_url || null
  } catch {
    return null
  }
})

const trackName = computed(() => {
  if (!currentStyle.value?.audio_metadata) return currentStyle.value?.name || ''
  try {
    const meta = JSON.parse(currentStyle.value.audio_metadata)
    return meta.track_name || currentStyle.value?.name || ''
  } catch {
    return currentStyle.value?.name || ''
  }
})

const artistName = computed(() => {
  if (!currentStyle.value?.audio_metadata) return ''
  try {
    const meta = JSON.parse(currentStyle.value.audio_metadata)
    return meta.artist_name || ''
  } catch {
    return ''
  }
})

const progress = computed(() => {
  if (!duration.value) return 0
  return currentTime.value / duration.value
})

const sliderStyle = computed(() => ({
  '--progress': `${(progress.value * 100).toFixed(2)}%`,
}))

function formatTime(seconds: number): string {
  if (!seconds || !isFinite(seconds)) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

function onSliderInput(e: Event) {
  const target = e.target as HTMLInputElement
  const ratio = parseFloat(target.value)
  seek(ratio * duration.value)
}
</script>

<template>
  <Transition
    enter-active-class="transition-transform duration-300 ease-out"
    leave-active-class="transition-transform duration-200 ease-in"
    enter-from-class="translate-y-full"
    leave-to-class="translate-y-full"
  >
    <div
      v-if="show"
      class="pointer-events-auto fixed bottom-0 left-0 right-0 z-40
             bg-void/95 backdrop-blur-md border-t-2 border-neon-cyan/40
             px-3 py-2.5 flex items-center gap-3"
    >
      <!-- Album art / spinning disc -->
      <div class="w-10 h-10 rounded-full flex-shrink-0 overflow-hidden border-2 border-neon-cyan/60 relative">
        <img
          v-if="artwork"
          :src="artwork"
          alt=""
          class="w-full h-full object-cover"
        />
        <div
          v-else
          class="w-full h-full bg-neon-cyan/20 flex items-center justify-center"
        >
          <svg class="w-5 h-5 text-neon-cyan/70" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
          </svg>
        </div>
        <!-- Spinning overlay -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-3 h-3 rounded-full bg-void/80 border border-neon-cyan/40 animate-spin-slow"></div>
        </div>
      </div>

      <!-- Track info -->
      <div class="flex-1 min-w-0 hidden sm:block max-w-[140px]">
        <div class="text-xs text-neon-cyan font-mono truncate leading-tight">{{ trackName }}</div>
        <div class="text-[10px] text-chrome/60 font-mono truncate">{{ artistName }}</div>
      </div>

      <!-- Progress slider -->
      <div class="flex items-center gap-2 flex-1 min-w-0" :style="sliderStyle">
        <span class="text-[10px] text-chrome/60 font-mono w-8 text-right flex-shrink-0">{{ formatTime(currentTime) }}</span>
        <input
          type="range"
          min="0"
          max="1"
          step="0.001"
          :value="progress"
          @input="onSliderInput"
          class="audio-slider flex-1 h-1 cursor-pointer"
        />
        <span class="text-[10px] text-chrome/60 font-mono w-8 flex-shrink-0">{{ formatTime(duration) }}</span>
      </div>

      <!-- Stop button -->
      <button
        @click="stop"
        class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0
               border-2 border-neon-magenta bg-neon-magenta/20 text-neon-magenta
               hover:bg-neon-magenta hover:text-white transition-all duration-200"
        title="停止"
      >
        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="6" width="12" height="12" rx="1"/>
        </svg>
      </button>
    </div>
  </Transition>
</template>

<style scoped>
/* ── Range slider ── */
.audio-slider {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  outline: none;
}

/* Track: WebKit */
.audio-slider::-webkit-slider-runnable-track {
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(
    to right,
    #00f0ff var(--progress, 0%),
    rgba(255, 255, 255, 0.15) var(--progress, 0%),
    rgba(255, 255, 255, 0.15) 100%
  );
}

/* Track: Firefox */
.audio-slider::-moz-range-track {
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.15);
}

.audio-slider::-moz-range-progress {
  height: 4px;
  border-radius: 2px;
  background: #00f0ff;
}

/* Thumb: WebKit */
.audio-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #00f0ff;
  border: 2px solid #0a0a0f;
  cursor: pointer;
  margin-top: -5px;
  box-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}

/* Thumb: Firefox */
.audio-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #00f0ff;
  border: 2px solid #0a0a0f;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}

/* Slow spin for disc overlay */
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}
</style>
