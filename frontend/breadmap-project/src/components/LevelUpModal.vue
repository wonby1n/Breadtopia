<template>
  <Transition name="modal-fade">
    <div
      v-if="show"
      class="fixed inset-0 z-[9999] flex items-center justify-center"
      @click="handleClose"
    >
      <!-- 흐린 배경 -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-md"></div>

      <!-- 모달 컨텐츠 -->
      <div
        class="relative z-10 bg-gradient-to-br from-[#FFFDF9] to-[#F9F7F2] rounded-3xl shadow-2xl p-8 md:p-12 max-w-md w-full mx-4 transform"
        @click.stop
      >
        <!-- 폭죽 애니메이션 -->
        <div class="confetti-container">
          <div v-for="i in 50" :key="i" class="confetti" :style="getConfettiStyle(i)"></div>
        </div>

        <!-- 레벨업 텍스트 -->
        <div class="text-center mb-6 animate-bounce-in">
          <h1 class="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 mb-2 animate-gradient">
            LEVEL UP!
          </h1>
          <p class="text-2xl font-bold text-[#4E342E] animate-slide-up">
            축하드립니다! 🎉
          </p>
        </div>

        <!-- 레벨 변화 -->
        <div class="flex items-center justify-center gap-4 mb-8 animate-slide-up-delay-1">
          <div class="text-center">
            <div class="text-4xl font-black text-gray-400">Lv.{{ levelInfo?.oldLevel }}</div>
            <div class="text-sm text-gray-500 mt-1">{{ getCharacter(levelInfo?.oldLevel).name }}</div>
          </div>

          <div class="text-4xl text-[#8BC34A] animate-pulse">→</div>

          <div class="text-center">
            <div class="text-5xl font-black text-[#8BC34A] animate-scale-up">
              Lv.{{ levelInfo?.newLevel }}
            </div>
            <div class="text-sm text-[#558B2F] mt-1 font-bold">{{ levelInfo?.character.name }}</div>
          </div>
        </div>

        <!-- 새 캐릭터 이미지 -->
        <div class="flex justify-center mb-6 animate-slide-up-delay-2">
          <div class="relative">
            <!-- 빛나는 효과 -->
            <div class="absolute inset-0 bg-yellow-300/30 rounded-full blur-3xl animate-pulse-slow"></div>

            <!-- 캐릭터 이미지 -->
            <div class="relative w-40 h-40 bg-white rounded-full border-8 border-[#8BC34A] shadow-2xl flex items-center justify-center overflow-hidden transform hover:scale-110 transition-transform duration-300">
              <img
                :src="levelInfo?.character.img"
                :alt="levelInfo?.character.name"
                class="w-32 h-32 object-contain drop-shadow-lg animate-float"
              />
            </div>

            <!-- 회전하는 별 -->
            <div class="absolute -top-2 -right-2 text-4xl animate-spin-slow">⭐</div>
            <div class="absolute -bottom-2 -left-2 text-3xl animate-spin-slow" style="animation-delay: 0.5s">✨</div>
          </div>
        </div>

        <!-- 새 캐릭터 정보 -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-4 mb-6 border-2 border-[#8BC34A] animate-slide-up-delay-3">
          <p class="text-center text-lg font-bold text-[#4E342E] mb-2">
            새로운 칭호를 획득했습니다!
          </p>
          <div class="flex items-center justify-center gap-2">
            <span class="text-4xl">{{ levelInfo?.character.icon }}</span>
            <span class="text-2xl font-black text-[#558B2F]">
              {{ levelInfo?.character.name }}
            </span>
          </div>
        </div>

        <!-- 닫기 버튼 -->
        <button
          @click="handleClose"
          class="w-full bg-gradient-to-r from-[#8BC34A] to-[#7CB342] text-white font-bold py-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 animate-slide-up-delay-4"
        >
          확인 🎊
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  levelInfo: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close']);

const handleClose = () => {
  emit('close');
};

// 레벨별 캐릭터 정보 (auth store와 동일)
const getCharacter = (level) => {
  const LEVEL_CONFIG = {
    1: { name: '아기빵쥐', icon: '🐭', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
    2: { name: '식빵햄찌', icon: '🐹', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
    3: { name: '호빵토끼', icon: '🐰', img: 'https://cdn-icons-png.flaticon.com/512/235/235372.png' },
    4: { name: '모닝코기', icon: '🐶', img: 'https://cdn-icons-png.flaticon.com/512/235/235415.png' },
    5: { name: '크루아상여우', icon: '🦊', img: 'https://cdn-icons-png.flaticon.com/512/235/235368.png' },
    6: { name: '브리오슈곰', icon: '🐻', img: 'https://cdn-icons-png.flaticon.com/512/235/235388.png' },
    7: { name: '사워도우울프', icon: '🐺', img: 'https://cdn-icons-png.flaticon.com/512/235/235356.png' },
    8: { name: '초코표범', icon: '🐆', img: 'https://cdn-icons-png.flaticon.com/512/235/235377.png' },
    9: { name: '바게트호크', icon: '🦅', img: 'https://cdn-icons-png.flaticon.com/512/235/235386.png' },
    10: { name: '황금밀 유니콘', icon: '🦄', img: 'https://cdn-icons-png.flaticon.com/512/235/235359.png' }
  };
  return LEVEL_CONFIG[level] || LEVEL_CONFIG[1];
};

// 폭죽 위치 랜덤 생성
const getConfettiStyle = (index) => {
  const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE'];
  const randomColor = colors[index % colors.length];
  const randomX = Math.random() * 100;
  const randomDelay = Math.random() * 2;
  const randomDuration = 2 + Math.random() * 2;

  return {
    left: `${randomX}%`,
    backgroundColor: randomColor,
    animationDelay: `${randomDelay}s`,
    animationDuration: `${randomDuration}s`
  };
};
</script>

<style scoped>
/* 모달 페이드 인/아웃 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .relative {
  animation: zoomIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.3);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 폭죽 애니메이션 */
.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  border-radius: 1.5rem;
}

.confetti {
  position: absolute;
  width: 10px;
  height: 10px;
  top: -10px;
  border-radius: 50%;
  animation: confettiFall linear infinite;
}

@keyframes confettiFall {
  to {
    transform: translateY(120vh) rotate(360deg);
  }
}

/* 바운스 인 애니메이션 */
.animate-bounce-in {
  animation: bounceIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* 슬라이드 업 애니메이션 */
.animate-slide-up {
  animation: slideUp 0.6s ease-out 0.2s both;
}

.animate-slide-up-delay-1 {
  animation: slideUp 0.6s ease-out 0.4s both;
}

.animate-slide-up-delay-2 {
  animation: slideUp 0.6s ease-out 0.6s both;
}

.animate-slide-up-delay-3 {
  animation: slideUp 0.6s ease-out 0.8s both;
}

.animate-slide-up-delay-4 {
  animation: slideUp 0.6s ease-out 1s both;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 스케일 업 애니메이션 */
.animate-scale-up {
  animation: scaleUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s both;
}

@keyframes scaleUp {
  from {
    transform: scale(0.5);
  }
  to {
    transform: scale(1);
  }
}

/* 플로팅 애니메이션 */
.animate-float {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 느린 회전 */
.animate-spin-slow {
  animation: spin 4s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 느린 펄스 */
.animate-pulse-slow {
  animation: pulseSlow 3s ease-in-out infinite;
}

@keyframes pulseSlow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

/* 그라디언트 애니메이션 */
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

@keyframes gradient {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}
</style>
