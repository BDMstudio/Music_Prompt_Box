import { ref, onUnmounted } from 'vue'
import type { Style } from '@/types'

const globalAudio = new Audio()
const currentPlayingId = ref<string | null>(null)
const isPlaying = ref(false)

globalAudio.addEventListener('ended', () => {
  currentPlayingId.value = null
  isPlaying.value = false
})

globalAudio.addEventListener('pause', () => {
  isPlaying.value = false
})

globalAudio.addEventListener('play', () => {
  isPlaying.value = true
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
      return
    }

    globalAudio.src = url
    globalAudio.play()
    currentPlayingId.value = id
  }

  function playStyle(style: Style) {
    const url = resolveAudioUrl(style)
    if (!url) return
    play(style.id, url)
  }

  function stop() {
    globalAudio.pause()
    globalAudio.currentTime = 0
    currentPlayingId.value = null
  }

  function isCurrentlyPlaying(id: string): boolean {
    return currentPlayingId.value === id && isPlaying.value
  }

  return {
    currentPlayingId,
    isPlaying,
    play,
    playStyle,
    stop,
    isCurrentlyPlaying,
    resolveAudioUrl,
  }
}
