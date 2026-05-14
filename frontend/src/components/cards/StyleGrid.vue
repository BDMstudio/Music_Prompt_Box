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
    <!-- Loading -->
    <div v-if="stylesStore.loading" class="flex items-center justify-center py-20">
      <div class="w-10 h-10 border-4 border-foreground dark:border-dark-border border-t-primary-red animate-spin"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="stylesStore.styles.length === 0" class="text-center py-20 text-text-sub dark:text-dark-text-sub">
      <div class="w-16 h-16 geo-circle bg-muted dark:bg-dark-muted mx-auto mb-4 flex items-center justify-center">
        <svg class="w-8 h-8 text-text-sub dark:text-dark-text-sub" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <p class="font-bold uppercase tracking-wider text-foreground dark:text-dark-text-main">没有找到匹配的风格</p>
      <p class="text-sm mt-1 font-medium">尝试其他搜索词或筛选条件</p>
    </div>

    <!-- Content -->
    <div v-else>
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <StyleCard
          v-for="style in stylesStore.styles"
          :key="style.id"
          :style="style"
        />
      </div>

      <!-- Pagination -->
      <div v-if="stylesStore.total > stylesStore.size" class="flex items-center justify-center gap-4 mt-8">
        <button
          @click="prevPage"
          :disabled="stylesStore.page <= 1"
          class="px-4 py-2 border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface font-bold uppercase tracking-wider text-sm
                 text-foreground dark:text-dark-text-main
                 disabled:opacity-50 disabled:cursor-not-allowed
                 shadow-hard-sm dark:shadow-dark-hard-sm hover:bg-muted dark:hover:bg-dark-muted
                 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
        >
          上一页
        </button>
        <span class="text-sm font-bold uppercase tracking-widest text-text-sub dark:text-dark-text-sub">
          第 {{ stylesStore.page }} 页 / 共 {{ Math.ceil(stylesStore.total / stylesStore.size) }} 页
        </span>
        <button
          @click="nextPage"
          :disabled="stylesStore.page >= Math.ceil(stylesStore.total / stylesStore.size)"
          class="px-4 py-2 border-2 border-foreground dark:border-dark-border bg-white dark:bg-dark-surface font-bold uppercase tracking-wider text-sm
                 text-foreground dark:text-dark-text-main
                 disabled:opacity-50 disabled:cursor-not-allowed
                 shadow-hard-sm dark:shadow-dark-hard-sm hover:bg-muted dark:hover:bg-dark-muted
                 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none transition-all duration-200"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
