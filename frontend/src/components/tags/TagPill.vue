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
    class="px-2 py-1 text-xs font-mono bg-accent/10 text-purple-300 rounded border border-transparent hover:border-accent/50 hover:bg-accent/20 hover:text-white transition"
  >
    {{ tag }}
  </button>
</template>
