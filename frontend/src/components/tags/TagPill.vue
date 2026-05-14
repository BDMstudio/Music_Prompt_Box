<script setup lang="ts">
import { useClipboard } from '@/composables/useClipboard'
import { useTagsStore } from '@/stores/tags'

const props = defineProps<{
  tag: string
}>()

const { copy } = useClipboard()
const tagsStore = useTagsStore()

async function copyTag() {
  await copy(props.tag, `"${props.tag}" 已复制`)
  tagsStore.recordCopies([props.tag])
}
</script>

<template>
  <button
    @click="copyTag"
    class="px-2 py-1 text-xs font-mono bg-panel-solid text-neon-cyan border border-neon-cyan/30
           hover:bg-neon-cyan hover:text-void hover:shadow-neon-cyan
           transition-all duration-200 uppercase tracking-wider"
  >
    {{ tag }}
  </button>
</template>
