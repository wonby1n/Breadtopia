<template>
  <footer class="bg-[#FFF3DD] py-20 border-t border-[#F3B37A]/30 relative font-jua">
    <div class="max-w-[1400px] mx-auto px-6 md:px-12 relative z-10">
      <div class="flex flex-col md:flex-row justify-between items-start gap-10">
        <div class="space-y-4">
          <!-- 로고 및 타이틀 -->
          <div class="flex items-center gap-2 mb-2">
            <img
              :src="logoImage"
              alt="Breadtopia Logo"
              class="w-10 h-10 object-contain transition-transform duration-500 group-hover:rotate-12"
            />
            <h2 class="text-3xl font-bold text-[#6B4A38]">Breadtopia</h2>
          </div> 

          <p class="text-[#8B6A55] text-base leading-relaxed max-w-sm">
            전국 빵순이 빵돌이를 위한<br />
            가장 몽글몽글한 빵지순례 가이드.<br />
            오늘의 가장 맛있는 발견을 도와드려요. 🥨
          </p>
        </div>

        <div class="flex gap-16 text-sm font-medium">
          <div class="flex flex-col gap-4">
            <!-- 섹션 헤더 -->
            <span class="text-[#C99768] text-xs font-bold uppercase tracking-widest">
              Platform
            </span>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">About</a>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">Careers</a>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">Press</a>
          </div>
          <div class="flex flex-col gap-4">
            <span class="text-[#C99768] text-xs font-bold uppercase tracking-widest">
              Support
            </span>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">Contact</a>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">Privacy</a>
            <a href="#" class="text-[#8B6A55] hover:text-[#C99768] transition-colors">Terms</a>
          </div>
        </div>
      </div>

      <!-- 하단 카피라이트 영역 -->
      <div class="mt-20 pt-8 border-t border-[#6B4A38]/10 flex flex-col md:flex-row justify-between items-center text-xs text-[#8B6A55]/60">
        <p>© 2024 Breadtopia. All rights reserved.</p>
        <p class="flex items-center gap-1">
          Baked with Love & Flour
          <span>🌾</span>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import logoImage from '@/assets/images/logo.png'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}
</style>