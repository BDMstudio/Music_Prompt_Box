export interface Genre {
  id: string
  name: string
  parent_id: string | null
  level: number
  sort_order: number
  description: string | null
  era_prompt: string | null
  created_at: string
  updated_at: string
  children: Genre[]
}

export interface Style {
  id: string
  name: string
  tags: string[]
  genre_id: string | null
  genre_name: string | null
  description: string | null
  bpm_range: string | null
  audio_type: 'local' | 'url' | null
  audio_source: string | null
  audio_platform: 'local' | 'url' | 'itunes' | null
  audio_metadata: string | null  // JSON string
  reference_url: string | null
  copy_count: number
  is_favorited: boolean
  created_at: string
  updated_at: string
}

export interface StyleListResponse {
  total: number
  page: number
  size: number
  items: Style[]
}

export interface Folder {
  id: string
  name: string
  style_count: number
  created_at: string
  updated_at: string
}

export interface TagStat {
  tag: string
  copy_count: number
  last_copied_at: string | null
}

export interface StyleCreateInput {
  name: string
  tags: string[]
  genre_id?: string | null
  description?: string | null
  bpm_range?: string | null
  audio_type?: 'local' | 'url' | null
  audio_source?: string | null
  audio_platform?: 'local' | 'url' | 'itunes' | null
  audio_metadata?: string | null
  reference_url?: string | null
}

export interface StyleUpdateInput {
  name?: string
  tags?: string[]
  genre_id?: string | null
  description?: string | null
  bpm_range?: string | null
  audio_type?: 'local' | 'url' | null
  audio_source?: string | null
  audio_platform?: 'local' | 'url' | 'itunes' | null
  audio_metadata?: string | null
  reference_url?: string | null
}

export interface FolderCreateInput {
  name: string
}

export interface ExportData {
  version: string
  exported_at: string
  data: {
    genres: Genre[]
    styles: Style[]
    folders: Array<{
      id: string
      name: string
      style_ids: string[]
    }>
  }
}

// iTunes Search API types
export interface ITuneTrack {
  track_id: number
  track_name: string
  artist_name: string
  collection_name: string | null
  preview_url: string | null
  artwork_url100: string | null
  artwork_url600: string | null
  track_time_ms: number | null
  primary_genre_name: string | null
  country: string | null
}

export interface ITuneSearchResponse {
  result_count: number
  tracks: ITuneTrack[]
}

export interface ITuneAudioMetadata {
  platform: 'itunes'
  track_id: number
  track_name: string
  artist_name: string
  artwork_url: string | null
  preview_url: string | null
}
