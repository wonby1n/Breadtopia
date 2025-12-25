<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- ✅ meta.hideNavbar가 true가 아닐 때만 헤더 표시 -->
    <GlobalHeader v-if="!$route.meta.hideNavbar" />

    <main class="flex-grow">
      <router-view />
    </main>
    <BakeryChatbot />
    <!-- ✅ 지도 화면에서는 보통 푸터도 안 보이게 설정합니다 (필요하면 v-if 제거하세요) -->
    <GlobalFooter v-if="!$route.meta.hideNavbar" />

    <!-- ✅ 전역 레벨업 모달 -->
    <LevelUpModal
      :show="authStore.showLevelUpModal"
      :levelInfo="authStore.levelUpInfo"
      @close="authStore.closeLevelUpModal"
    />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import GlobalHeader from '@/components/GlobalHeader.vue'
import GlobalFooter from '@/components/GlobalFooter.vue'
import BakeryChatbot from '@/components/common/BakeryChatbot.vue'
import LevelUpModal from '@/components/LevelUpModal.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style>
@import 'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap';

body {
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #F9F7F2;
  color: #4A4036;
  overflow-x: hidden;
}

.font-playfair { font-family: 'Playfair Display', serif; }
.reveal-hidden { 
  opacity: 0; 
  transform: translateY(60px); 
  transition: all 1.2s cubic-bezier(0.22, 1, 0.36, 1); 
}
.reveal-visible { 
  opacity: 1; 
  transform: translateY(0); 
}

.img-zoom-container { overflow: hidden; }
.img-zoom-container img { 
  transition: transform 1.5s cubic-bezier(0.22, 1, 0.36, 1); 
}
.group:hover .img-zoom-container img { transform: scale(1.1); }

.delay-100 { transition-delay: 100ms; }
.delay-200 { transition-delay: 200ms; }
.delay-300 { transition-delay: 300ms; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #F0EBE0; }
::-webkit-scrollbar-thumb { background: #1D4E45; border-radius: 4px; }
</style>
