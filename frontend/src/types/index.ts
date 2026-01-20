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
