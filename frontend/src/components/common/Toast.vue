<script setup lang="ts">
import { useClipboard } from '@/composables/useClipboard'

const { showToast, toastMessage } = useClipboard()
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-4 opacity-0"
    >
      <div
        v-if="showToast"
        class="fixed bottom-5 right-5 px-4 py-2 bg-primary-blue text-white border-2 border-foreground dark:border-dark-border shadow-hard-sm dark:shadow-dark-hard-sm flex items-center gap-2 z-50 transition-colors duration-300"
      >
        <div class="w-4 h-4 geo-circle bg-primary-yellow flex-shrink-0"></div>
        <span class="font-bold uppercase tracking-wider text-sm">{{ toastMessage }}</span>
      </div>
    </Transition>
  </Teleport>
</template>
