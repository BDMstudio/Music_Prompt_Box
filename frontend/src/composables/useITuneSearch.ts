import { ref } from 'vue'
import type { ITuneTrack, ITuneAudioMetadata } from '@/types'
import { searchITunes } from '@/api/itunes'

export function useITuneSearch() {
  const tracks = ref<ITuneTrack[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function search(term: string, genre?: string) {
    if (!term.trim()) {
      tracks.value = []
      return
    }

    loading.value = true
    error.value = null
    try {
      const response = await searchITunes(term, { genre, limit: 10 })
      tracks.value = response.tracks
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'iTunes search failed'
      tracks.value = []
    } finally {
      loading.value = false
    }
  }

  function trackToMetadata(track: ITuneTrack): string {
    const meta: ITuneAudioMetadata = {
      platform: 'itunes',
      track_id: track.track_id,
      track_name: track.track_name,
      artist_name: track.artist_name,
      artwork_url: track.artwork_url600 || track.artwork_url100,
      preview_url: track.preview_url,
    }
    return JSON.stringify(meta)
  }

  function getPreviewUrl(metadataStr: string | null): string | null {
    if (!metadataStr) return null
    try {
      const meta: ITuneAudioMetadata = JSON.parse(metadataStr)
      return meta.preview_url
    } catch {
      return null
    }
  }

  function clear() {
    tracks.value = []
    error.value = null
  }

  return {
    tracks,
    loading,
    error,
    search,
    trackToMetadata,
    getPreviewUrl,
    clear,
  }
}
