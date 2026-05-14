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
      <div class="absolute inset-0 bg-void/80" @click="emit('cancel')"></div>
      
      <div class="relative border-2 border-neon-magenta bg-black/80 shadow-neon-magenta-lg w-full max-w-sm">
        <div class="flex items-center gap-2 px-4 py-2 bg-neon-magenta/10 border-b border-neon-magenta">
          <div class="h-3 w-3 rounded-full bg-neon-magenta"></div>
          <div class="h-3 w-3 rounded-full bg-neon-cyan"></div>
          <div class="h-3 w-3 rounded-full bg-neon-orange"></div>
          <span class="ml-2 text-xs font-mono text-neon-magenta/60">confirm.exe</span>
        </div>

        <div class="p-6">
          <h3 class="font-heading font-bold text-xl uppercase tracking-wider text-neon-magenta glow-text-magenta mb-2">{{ title }}</h3>
          <p class="text-chrome/70 text-sm font-mono mb-6">{{ message }}</p>
          
          <div class="flex justify-end gap-3">
            <button
              @click="emit('cancel')"
              class="-skew-x-12 border-2 border-neon-cyan bg-transparent text-neon-cyan font-mono uppercase tracking-wider text-sm px-4 py-2
                     hover:skew-x-0 hover:bg-neon-cyan hover:text-void hover:shadow-neon-cyan transition-all duration-200"
            >
              <span class="inline-block skew-x-12">{{ cancelText || '取消' }}</span>
            </button>
            <button
              @click="emit('confirm')"
              class="-skew-x-12 border-2 border-neon-magenta bg-neon-magenta text-white font-mono uppercase tracking-wider text-sm px-4 py-2
                     hover:skew-x-0 hover:scale-105 hover:shadow-neon-magenta-lg transition-all duration-200"
            >
              <span class="inline-block skew-x-12">{{ confirmText || '确认' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
