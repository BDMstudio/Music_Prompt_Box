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
      <div class="absolute inset-0 bg-foreground/60 dark:bg-black/70" @click="emit('cancel')"></div>
      
      <div class="relative bg-white dark:bg-dark-surface border-4 border-foreground dark:border-dark-border p-6 w-full max-w-sm shadow-hard-lg dark:shadow-dark-hard-lg transition-colors duration-300">
        <h3 class="text-xl font-black uppercase tracking-tighter text-foreground dark:text-dark-text-main mb-2">{{ title }}</h3>
        <p class="text-text-sub dark:text-dark-text-sub text-sm font-medium mb-6">{{ message }}</p>
        
        <div class="flex justify-end gap-3">
          <button
            @click="emit('cancel')"
            class="px-4 py-2 text-sm font-bold uppercase tracking-wider border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface shadow-hard-sm dark:shadow-dark-hard-sm
                   text-foreground dark:text-dark-text-main
                   hover:bg-muted dark:hover:bg-dark-muted active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
          >
            {{ cancelText || '取消' }}
          </button>
          <button
            @click="emit('confirm')"
            class="px-4 py-2 text-sm font-bold uppercase tracking-wider bg-primary-red text-white border-2 border-foreground dark:border-dark-border shadow-hard-sm dark:shadow-dark-hard-sm
                   hover:bg-primary-red/90 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
          >
            {{ confirmText || '确认' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
