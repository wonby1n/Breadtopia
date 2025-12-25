<template>
  <div class="min-h-screen bg-[#F9F7F2] pt-32 pb-32 relative overflow-hidden font-sans">
    
    <!-- ☁️ 몽글몽글 배경 효과 (Blobs) -->
    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-lime-200/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob pointer-events-none"></div>
    <div class="absolute top-[20%] right-[-10%] w-96 h-96 bg-green-100/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000 pointer-events-none"></div>
    <div class="absolute bottom-[-10%] left-[20%] w-96 h-96 bg-yellow-100/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000 pointer-events-none"></div>
    <!-- 종이 질감 오버레이 -->
    <div class="absolute inset-0 opacity-40 bg-[url('https://www.transparenttextures.com/patterns/cream-paper.png')] pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 space-y-8 relative z-10">
      
      <!-- 공통 헤더 -->
      <div class="text-center lg:text-left mb-10">
        <div class="inline-block relative">
          <h1 class="text-4xl md:text-5xl font-serif font-bold text-[#4E342E] mb-2 tracking-tight relative z-10">
            Community
          </h1>
          <!-- 밑줄 효과 -->
          <div class="absolute bottom-2 left-0 w-full h-3 bg-[#DCEDC8] -z-0 opacity-60 rounded-full transform -rotate-1"></div>
        </div>
        <p class="text-lg text-[#8D6E63] font-medium mt-2 flex items-center justify-center lg:justify-start gap-2">
          <span>🥐</span> 빵을 사랑하는 사람들의 따뜻한 수다 공간
        </p>
      </div>

      <!-- 모바일: 상세 보기 모드일 때 상단 뒤로가기 바 -->
      <div
        v-if="selectedPost && isMobile"
        class="flex items-center gap-3 py-3 border-b border-[#D7CCC8]/50 lg:hidden mb-4"
      >
        <button
          type="button"
          class="flex items-center gap-1 text-sm text-[#558B2F] font-bold hover:bg-[#F1F8E9] px-3 py-1 rounded-full transition-colors"
          @click="backToList"
        >
          <span class="text-lg">←</span>
          <span>목록으로</span>
        </button>
        <span class="text-xs text-[#A1887F] font-medium">/ {{ currentCategoryLabel }}</span>
      </div>

      <!-- 데스크톱 레이아웃 -->
      <div class="hidden lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- 리스트 영역 -->
        <section
          :class="[
            'space-y-6 transition-all duration-500 ease-in-out',
            selectedPost ? 'lg:col-span-1' : 'lg:col-span-3',
          ]"
        >
          <!-- 카테고리 탭 (동글동글 디자인) -->
          <div class="flex flex-wrap justify-center lg:justify-start gap-3 p-1">
            <button
              v-for="cat in categories"
              :key="cat.value"
              @click="handleCategoryChange(cat.value)"
              :class="[
                'px-5 py-2.5 text-sm font-bold rounded-full transition-all duration-300 flex items-center gap-2 shadow-sm',
                selectedCategory === cat.value
                  ? 'bg-[#8BC34A] text-white shadow-md transform scale-105'
                  : 'bg-white text-[#8D6E63] border border-[#E0E0E0] hover:bg-[#F1F8E9] hover:text-[#558B2F] hover:border-[#DCEDC8]',
              ]"
            >
              <span :class="['w-2 h-2 rounded-full', selectedCategory === cat.value ? 'bg-white' : 'bg-[#DCEDC8]']"></span>
              {{ cat.label }}
            </button>
          </div>

          <!-- 카테고리별 리스트 컴포넌트 (카드형 컨테이너 안에 넣어서 깔끔하게) -->
          <div class="bg-white/60 backdrop-blur-sm rounded-3xl p-2 border border-white/60 shadow-lg min-h-[500px]">
             <ChatterList
               v-if="selectedCategory === 'chatter'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <RecommendList
               v-else-if="selectedCategory === 'recommend'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <TipList
               v-else-if="selectedCategory === 'tip'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <HotList
               v-else
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
          </div>
        </section>

        <!-- 상세 영역 (데스크톱) -->
        <Transition name="slide-detail">
          <section v-if="selectedPost" class="lg:col-span-2">
            <!-- 상세 카드 (높이 고정 및 스크롤) -->
            <div class="bg-white rounded-[32px] shadow-2xl overflow-hidden border border-[#F0F4C3] sticky top-24 h-[calc(100vh-7.5rem)]">
               <DetailCard
                 :post="selectedPost"
                 :is-comments-open="isCommentsOpen"
                 :new-comment="newComment"
                 @update:isCommentsOpen="isCommentsOpen = $event"
                 @update:newComment="newComment = $event"
                 @close="backToList"
               />
            </div>
          </section>
        </Transition>
      </div>

      <!-- 모바일/태블릿 레이아웃 -->
      <div class="lg:hidden">
        <!-- 상세 보기 모드 -->
        <section v-if="selectedPost">
          <Transition name="slide-detail-mobile">
            <div class="bg-white rounded-[32px] shadow-xl overflow-hidden border border-[#F0F4C3] min-h-[70vh]">
               <DetailCard
                 :post="selectedPost"
                 :is-comments-open="isCommentsOpen"
                 :new-comment="newComment"
                 @update:isCommentsOpen="isCommentsOpen = $event"
                 @update:newComment="newComment = $event"
                 @close="backToList"
               />
            </div>
          </Transition>
        </section>

        <!-- 리스트 모드 -->
        <section v-else class="space-y-6">
          <!-- 카테고리 탭 -->
          <div class="flex flex-wrap justify-center gap-2 overflow-x-auto hide-scrollbar py-2">
            <button
              v-for="cat in categories"
              :key="cat.value"
              @click="handleCategoryChange(cat.value)"
              :class="[
                'px-4 py-2 text-xs font-bold rounded-full transition-all duration-200 flex items-center gap-1.5 whitespace-nowrap',
                selectedCategory === cat.value
                  ? 'bg-[#8BC34A] text-white shadow-md'
                  : 'bg-white text-[#8D6E63] border border-[#E0E0E0]',
              ]"
            >
              {{ cat.label }}
            </button>
          </div>

          <!-- 리스트 컨테이너 -->
          <div class="bg-white/60 backdrop-blur-sm rounded-3xl p-1 border border-white/60 shadow-lg min-h-[400px]">
             <ChatterList
               v-if="selectedCategory === 'chatter'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <RecommendList
               v-else-if="selectedCategory === 'recommend'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <TipList
               v-else-if="selectedCategory === 'tip'"
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
             <HotList
               v-else
               :selected-post-id="selectedPost?.id"
               @select-post="handleSelectPost"
             />
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/axios'
import DetailCard from '@/components/community/DetailCard.vue'
import ChatterList from '@/components/community/ChatterList.vue'
import RecommendList from '@/components/community/RecommendList.vue'
import TipList from '@/components/community/TipList.vue'
import HotList from '@/components/community/HotList.vue'

const route = useRoute()
const router = useRouter()

const categories = [
  { value: 'hot', label: 'HOT 🔥' },
  { value: 'chatter', label: '빵 주저리 💬' },
  { value: 'recommend', label: '빵집 추천 🥐' },
  { value: 'tip', label: '빵 꿀팁 🍯' },
]

const selectedCategory = ref('hot')
const selectedPost = ref(null)
const isCommentsOpen = ref(false)
const newComment = ref('')

// ✅ URL 파라미터로 post ID가 전달되면 해당 게시글 로드
const loadPostById = async (postId) => {
  if (!postId) return

  try {
    const response = await apiClient.get(`/community/${postId}/`)
    selectedPost.value = response.data

    // 카테고리도 자동 선택
    const categoryMap = {
      '빵 주저리': 'chatter',
      '빵집 추천': 'recommend',
      '빵 꿀팁': 'tip'
    }
    if (response.data.category && categoryMap[response.data.category]) {
      selectedCategory.value = categoryMap[response.data.category]
    }
  } catch (error) {
    console.error('게시글 로드 실패:', error)
    alert('게시글을 불러올 수 없습니다.')
    router.push({ name: 'community' })
  }
}

// ✅ URL 파라미터 변경 감지
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadPostById(newId)
  } else {
    selectedPost.value = null
  }
})

const width = ref(window.innerWidth)
const onResize = () => {
  width.value = window.innerWidth
}

// ✅ 컴포넌트 마운트 시 초기화
onMounted(() => {
  window.addEventListener('resize', onResize)

  // URL 파라미터로 post ID가 있으면 해당 게시글 로드
  if (route.params.id) {
    loadPostById(route.params.id)
  }
})

onUnmounted(() => window.removeEventListener('resize', onResize))
const isMobile = computed(() => width.value < 1024)

const currentCategoryLabel = computed(() => {
  const cat = categories.find((c) => c.value === selectedCategory.value)
  return cat ? cat.label : ''
})

const handleCategoryChange = (categoryValue) => {
  selectedCategory.value = categoryValue
  selectedPost.value = null
  isCommentsOpen.value = false
}

const handleSelectPost = async (post) => {
  selectedPost.value = post
  isCommentsOpen.value = false

  if (isMobile.value) {
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const backToList = () => {
  selectedPost.value = null
  isCommentsOpen.value = false
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Gaegu:wght@400;700&display=swap');

/* 전체 폰트 적용 */
div {
  font-family: 'Noto Sans KR', sans-serif;
}

/* 제목 등 포인트 폰트 */
h1, .font-serif {
  font-family: 'Gaegu', cursive;
}

/* 몽글몽글 구름 애니메이션 */
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}

/* 슬라이드 애니메이션 */
.slide-detail-enter-active,
.slide-detail-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-detail-enter-from,
.slide-detail-leave-to {
  opacity: 0;
  transform: translateY(20px); /* 위아래로 부드럽게 */
}

/* 스크롤바 숨기기 */
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>