<script setup lang="ts">
import { useStylesStore } from '@/stores/styles'
import StyleCard from './StyleCard.vue'

const stylesStore = useStylesStore()

function prevPage() {
  if (stylesStore.page > 1) {
    stylesStore.setPage(stylesStore.page - 1)
  }
}

function nextPage() {
  const maxPage = Math.ceil(stylesStore.total / stylesStore.size)
  if (stylesStore.page < maxPage) {
    stylesStore.setPage(stylesStore.page + 1)
  }
}
</script>

<template>
  <div>
    <div v-if="stylesStore.loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="stylesStore.styles.length === 0" class="text-center py-20 text-text-sub">
      <svg class="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p>没有找到匹配的风格</p>
      <p class="text-sm mt-1">尝试其他搜索词或筛选条件</p>
    </div>

    <div v-else>
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
        <StyleCard
          v-for="style in stylesStore.styles"
          :key="style.id"
          :style="style"
        />
      </div>

      <div v-if="stylesStore.total > stylesStore.size" class="flex items-center justify-center gap-4 mt-8">
        <button
          @click="prevPage"
          :disabled="stylesStore.page <= 1"
          class="px-4 py-2 border border-zinc-700 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-zinc-800 transition"
        >
          上一页
        </button>
        <span class="text-sm text-text-sub">
          第 {{ stylesStore.page }} 页 / 共 {{ Math.ceil(stylesStore.total / stylesStore.size) }} 页
        </span>
        <button
          @click="nextPage"
          :disabled="stylesStore.page >= Math.ceil(stylesStore.total / stylesStore.size)"
          class="px-4 py-2 border border-zinc-700 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-zinc-800 transition"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
