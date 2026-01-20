import { ref, onUnmounted } from 'vue'

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
    stop,
    isCurrentlyPlaying,
  }
}
