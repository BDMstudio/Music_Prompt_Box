<script setup lang="ts">
defineProps<{
  title: string
  message: string
  confirmText?: string
  cancelText?: string
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/60" @click="emit('cancel')"></div>
      
      <div class="relative bg-card-bg border border-border rounded-xl p-6 w-full max-w-sm shadow-2xl">
        <h3 class="text-lg font-semibold text-white mb-2">{{ title }}</h3>
        <p class="text-text-sub text-sm mb-6">{{ message }}</p>
        
        <div class="flex justify-end gap-3">
          <button
            @click="emit('cancel')"
            class="px-4 py-2 text-sm border border-zinc-700 rounded-lg hover:bg-zinc-800 transition"
          >
            {{ cancelText || '取消' }}
          </button>
          <button
            @click="emit('confirm')"
            class="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 rounded-lg transition"
          >
            {{ confirmText || '确认' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
