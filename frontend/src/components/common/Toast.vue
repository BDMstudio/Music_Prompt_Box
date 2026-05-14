<script setup lang="ts">
import { useClipboard } from '@/composables/useClipboard'

const { showToast, toastMessage } = useClipboard()
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-linear"
      enter-from-class="translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-linear"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-4 opacity-0"
    >
      <div
        v-if="showToast"
        class="fixed bottom-5 right-5 px-4 py-2 bg-neon-cyan text-void border-2 border-neon-cyan shadow-neon-cyan
               flex items-center gap-2 z-50 font-mono uppercase tracking-wider text-sm"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        {{ toastMessage }}
      </div>
    </Transition>
  </Teleport>
</template>
