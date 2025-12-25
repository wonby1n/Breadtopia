<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { X, Image as ImageIcon } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const title = ref('')
const content = ref('')
const categoryValue = '빵 꿀팁' // 백엔드 모델에 저장될 값

const imageFile = ref(null)
const imagePreview = ref(null) // 이미지 미리보기 URL
const fileInputRef = ref(null) // input 태그 제어용
const isSubmitting = ref(false)

// 이미지 선택 핸들러
const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    imageFile.value = file
    // 미리보기 URL 생성
    imagePreview.value = URL.createObjectURL(file)
  }
}

// 🗑️ 이미지 삭제 함수
const removeImage = () => {
  imageFile.value = null
  imagePreview.value = null
  if (fileInputRef.value) {
    fileInputRef.value.value = '' // input 초기화
  }
}

const handleSubmit = async () => {
  if (!authStore.token) {
    alert('로그인이 필요한 기능입니다.')
    return
  }

  if (!title.value || !content.value) { 
    alert('제목과 내용을 입력해주세요.')
    return 
  }
  
  try {
    isSubmitting.value = true
    
    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('content', content.value)
    formData.append('category', categoryValue)
    
    if (imageFile.value) {
      formData.append('image', imageFile.value) // 백엔드 필드명 'image'와 일치
    }
    
    // API 요청 (헤더에 토큰 포함)
    await apiClient.post('/community/create/', formData, {
      headers: {
        'Authorization': `Token ${authStore.token}`,
        // multipart/form-data는 axios가 자동으로 설정하므로 생략
      }
    })

    // ✅ 경험치 획득으로 인한 레벨업 체크를 위해 사용자 정보 갱신
    await authStore.fetchUser()

    alert('꿀팁이 등록되었습니다! 🍯')
    router.push({ name: 'community' })

  } catch (e) { 
    console.error('API Error:', e)
    
    if (e.response?.status === 401) {
      alert('인증 정보가 만료되었습니다. 다시 로그인해주세요.')
    } else if (e.response?.status === 400) {
      alert('입력 정보를 확인해주세요.')
    } else {
      alert('오류가 발생했습니다.') 
    }
  } finally { 
    isSubmitting.value = false 
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] py-20 px-6 font-sans">
    <div class="max-w-4xl mx-auto space-y-8">
      <div class="text-center lg:text-left">
        <h1 class="text-4xl font-serif font-bold text-[#E65100] mb-2 tracking-wide flex items-center justify-center lg:justify-start gap-2">
          <span class="text-3xl">🍯</span> 빵 꿀팁 공유
        </h1>
        <p class="text-lg text-[#8D6E63] font-medium">나만 알기 아까운 빵 보관법, 더 맛있게 먹는 법을 알려주세요.</p>
      </div>

      <div class="bg-white rounded-[40px] shadow-2xl border border-[#FFCC80] p-8 md:p-12 relative overflow-hidden">
        <!-- 꿀 흐르는 효과 장식 -->
        <div class="absolute top-0 left-10 w-20 h-10 bg-[#FFB74D] rounded-b-3xl opacity-50"></div>
        <div class="absolute top-0 right-20 w-14 h-16 bg-[#FFE0B2] rounded-b-full opacity-50"></div>

        <div class="relative z-10 space-y-6">
          <div class="flex items-center gap-2 mb-6">
            <span class="px-4 py-1.5 bg-[#FFF3E0] text-[#EF6C00] text-xs font-bold rounded-full border border-[#FFCC80]">
              {{ categoryValue }}
            </span>
          </div>

          <div class="space-y-6">
            <label class="block text-left">
              <span class="text-sm font-bold text-[#E65100] mb-2 block">제목</span>
              <input v-model="title" type="text" class="w-full border border-[#FFE0B2] rounded-xl px-4 py-3 text-sm bg-[#FFF8E1] focus:outline-none focus:ring-2 focus:ring-[#FFB74D] placeholder-[#FFCC80] text-[#5D4037]" placeholder="예: 바게트 눅눅하지 않게 보관하는 법" />
            </label>

            <label class="block text-left">
              <span class="text-sm font-bold text-[#E65100] mb-2 block">내용</span>
              <textarea v-model="content" class="w-full border border-[#FFE0B2] rounded-xl px-4 py-3 text-sm min-h-[240px] bg-[#FFF8E1] focus:outline-none focus:ring-2 focus:ring-[#FFB74D] placeholder-[#FFCC80] text-[#5D4037] leading-relaxed resize-none" placeholder="자세한 팁을 적어주세요."></textarea>
            </label>

            <!-- 사진 첨부 영역 -->
            <label class="block text-left">
              <span class="text-sm font-bold text-[#E65100] mb-2 block">사진 첨부</span>
              
              <!-- 1. 파일 선택 전 -->
              <div v-if="!imageFile" class="relative group cursor-pointer w-full">
                <input 
                  ref="fileInputRef"
                  type="file" 
                  accept="image/*" 
                  @change="handleImageChange" 
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
                />
                <div class="w-full border-2 border-dashed border-[#FFCC80] rounded-xl p-8 text-center bg-[#FFF3E0] group-hover:bg-[#FFE0B2] transition-colors flex flex-col items-center gap-2">
                  <ImageIcon class="w-8 h-8 text-[#EF6C00] opacity-50" />
                  <p class="text-sm text-[#EF6C00] font-medium">
                    클릭하여 사진을 올려주세요 📸
                  </p>
                </div>
              </div>

              <!-- 2. 파일 선택 후 (미리보기 + 삭제 버튼) -->
              <div v-else class="relative w-full border-2 border-[#FFCC80] rounded-xl bg-[#FFF3E0] p-4 flex items-center gap-4">
                <!-- 썸네일 -->
                <div class="w-16 h-16 rounded-lg overflow-hidden bg-white border border-[#FFE0B2] shadow-sm flex-shrink-0">
                  <img :src="imagePreview" class="w-full h-full object-cover" />
                </div>
                
                <!-- 파일명 -->
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-[#E65100] font-bold truncate">{{ imageFile.name }}</p>
                  <p class="text-xs text-[#FB8C00]">업로드 준비 완료</p>
                </div>

                <!-- 🗑️ 삭제 버튼 -->
                <button 
                  @click.prevent="removeImage"
                  type="button"
                  class="p-2 bg-white text-[#EF6C00] hover:bg-[#FFCC80] hover:text-white rounded-full transition-colors shadow-sm border border-[#FFE0B2]"
                  title="사진 삭제"
                >
                  <X class="w-5 h-5" />
                </button>
              </div>
            </label>
          </div>

          <div class="mt-10 flex flex-col sm:flex-row justify-end gap-4 pt-6 border-t border-[#FFE0B2]">
            <button @click="router.go(-1)" class="px-8 py-3 border border-[#FFCC80] text-sm font-bold rounded-full text-[#EF6C00] hover:bg-[#FFF3E0]">취소</button>
            <button @click="handleSubmit" :disabled="isSubmitting" class="px-10 py-3 bg-[#EF6C00] text-white text-sm font-bold rounded-full hover:bg-[#E65100] disabled:bg-[#FFCC80] shadow-lg transform hover:-translate-y-1 transition-all">
              {{ isSubmitting ? '등록 중...' : '꿀팁 등록하기' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');
.font-serif { font-family: 'Gaegu', cursive; }
div { font-family: 'Noto Sans KR', sans-serif; }
</style>