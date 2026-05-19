import { ref, watch, onUnmounted } from 'vue'
import type { Style } from '@/types'

const globalAudio = new Audio()
const currentPlayingId = ref<string | null>(null)
const currentStyle = ref<Style | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)

// ── Audio event listeners ──

globalAudio.addEventListener('ended', () => {
  currentPlayingId.value = null
  currentStyle.value = null
  isPlaying.value = false
  currentTime.value = 0
})

globalAudio.addEventListener('pause', () => {
  isPlaying.value = false
})

globalAudio.addEventListener('play', () => {
  isPlaying.value = true
})

globalAudio.addEventListener('timeupdate', () => {
  currentTime.value = globalAudio.currentTime
})

globalAudio.addEventListener('loadedmetadata', () => {
  duration.value = globalAudio.duration || 0
})

globalAudio.addEventListener('durationchange', () => {
  duration.value = globalAudio.duration || 0
})

/**
 * Resolve the actual playable audio URL from a Style object.
 * - For 'itunes' platform: extract preview_url from audio_metadata JSON
 * - For 'url' or 'local': use audio_source directly
 */
function resolveAudioUrl(style: Style): string | null {
  if (style.audio_platform === 'itunes' && style.audio_metadata) {
    try {
      const meta = JSON.parse(style.audio_metadata)
      if (meta.preview_url) return meta.preview_url
    } catch { /* fall through */ }
  }
  return style.audio_source || null
}

export function useAudio() {
  function play(id: string, url: string) {
    if (currentPlayingId.value === id && !globalAudio.paused) {
      globalAudio.pause()
      currentPlayingId.value = null
      currentStyle.value = null
      return
    }

    globalAudio.src = url
    globalAudio.play()
    currentPlayingId.value = id
  }

  function playStyle(style: Style) {
    const url = resolveAudioUrl(style)
    if (!url) return
    currentStyle.value = style
    play(style.id, url)
  }

  function stop() {
    globalAudio.pause()
    globalAudio.currentTime = 0
    currentPlayingId.value = null
    currentStyle.value = null
  }

  function seek(time: number) {
    if (globalAudio.duration) {
      globalAudio.currentTime = Math.max(0, Math.min(time, globalAudio.duration))
    }
  }

  function isCurrentlyPlaying(id: string): boolean {
    return currentPlayingId.value === id && isPlaying.value
  }

  return {
    currentPlayingId,
    currentStyle,
    isPlaying,
    currentTime,
    duration,
    play,
    playStyle,
    stop,
    seek,
    isCurrentlyPlaying,
    resolveAudioUrl,
  }
}
