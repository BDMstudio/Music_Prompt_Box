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
    class="px-2 py-1 text-xs font-bold uppercase tracking-wider bg-primary-yellow/20 dark:bg-primary-yellow/30 text-foreground dark:text-dark-text-main border-2 border-transparent
           hover:border-foreground dark:hover:border-dark-border hover:bg-primary-yellow transition-all duration-200"
  >
    {{ tag }}
  </button>
</template>
