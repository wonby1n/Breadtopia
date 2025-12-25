<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { X } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const title = ref('')
const content = ref('')
const categoryLabel = '빵 주저리'
const categoryValue = '빵 주저리' // 백엔드 전송용 값

const imageFile = ref(null)
const fileInputRef = ref(null)
const isSubmitting = ref(false)

const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    console.log('이미지 선택:', file.name)
    imageFile.value = file
  }
}

// 🗑️ 이미지 삭제 함수
const removeImage = () => {
  imageFile.value = null
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
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
      formData.append('image', imageFile.value)
    }
    
    // 디버깅용
    console.log('전송 데이터:', { title: title.value, category: categoryValue, hasImage: !!imageFile.value })

    await apiClient.post('/community/create/', formData, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })

    // ✅ 경험치 획득으로 인한 레벨업 체크를 위해 사용자 정보 갱신
    await authStore.fetchUser()

    alert('이야기가 등록되었습니다! 🥐')
    router.push({ name: 'community' })

  } catch (e) { 
    console.error('API Error:', e)
    
    if (e.response) {
      const status = e.response.status
      const data = e.response.data

      if (status === 401) {
        alert('인증 정보가 유효하지 않습니다. 다시 로그인해주세요.')
      } else if (status === 400) {
        let errorMsg = '입력 정보를 확인해주세요:\n'
        if (typeof data === 'object') {
          for (const key in data) {
            errorMsg += `\n• ${key}: ${data[key]}`
          }
        } else {
          errorMsg += JSON.stringify(data)
        }
        alert(errorMsg)
      } else {
        alert(`서버 오류가 발생했습니다. (Code: ${status})`) 
      }
    } else {
      alert('네트워크 오류가 발생했습니다.')
    }
  } finally { 
    isSubmitting.value = false 
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] py-20 px-6 font-sans">
    <div class="max-w-4xl mx-auto space-y-8">
      
      <!-- 헤더 -->
      <div class="text-center lg:text-left">
        <h1 class="text-4xl font-serif font-bold text-[#4E342E] mb-2 tracking-wide flex items-center justify-center lg:justify-start gap-2">
          <span class="text-3xl">💬</span> 빵 주저리 작성
        </h1>
        <p class="text-lg text-[#8D6E63] font-medium">
          빵에 대한 소소하고 귀여운 이야기들을 들려주세요.
        </p>
      </div>

      <!-- 작성 폼 -->
      <div class="bg-white rounded-[40px] shadow-2xl border border-[#EFEBE9] p-8 md:p-12 relative overflow-hidden">
        <!-- 데코레이션 -->
        <div class="absolute top-0 right-0 w-32 h-32 bg-[#D7CCC8]/20 rounded-bl-full pointer-events-none"></div>
        <div class="absolute bottom-0 left-0 w-24 h-24 bg-[#FFCC80]/10 rounded-tr-full pointer-events-none"></div>

        <div class="relative z-10 space-y-6">
          <div class="flex items-center gap-2 mb-6">
            <span class="px-4 py-1.5 bg-[#EFEBE9] text-[#5D4037] text-xs font-bold rounded-full border border-[#D7CCC8]">
              {{ categoryLabel }}
            </span>
          </div>

          <div class="space-y-6">
            <label class="block text-left">
              <span class="text-sm font-bold text-[#5D4037] mb-2 block">제목</span>
              <input
                v-model="title"
                type="text"
                class="w-full border border-[#D7CCC8] rounded-xl px-4 py-3 text-sm bg-[#FAFAFA] focus:outline-none focus:ring-2 focus:ring-[#8D6E63] focus:border-transparent transition-all placeholder-[#BCAAA4]"
                placeholder="제목을 입력해주세요"
              />
            </label>

            <label class="block text-left">
              <span class="text-sm font-bold text-[#5D4037] mb-2 block">내용</span>
              <textarea
                v-model="content"
                class="w-full border border-[#D7CCC8] rounded-xl px-4 py-3 text-sm min-h-[240px] bg-[#FAFAFA] focus:outline-none focus:ring-2 focus:ring-[#8D6E63] focus:border-transparent transition-all placeholder-[#BCAAA4] leading-relaxed resize-none"
                placeholder="오늘 먹은 빵은 어땠나요? 자유롭게 적어주세요."
              ></textarea>
            </label>

            <label class="block text-left">
              <span class="text-sm font-bold text-[#5D4037] mb-2 block">사진 첨부</span>
              
              <!-- 파일 선택 전 -->
              <div v-if="!imageFile" class="relative group cursor-pointer">
                <input 
                  ref="fileInputRef"
                  type="file" 
                  accept="image/*" 
                  @change="handleImageChange" 
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
                />
                <div class="w-full border-2 border-dashed border-[#D7CCC8] rounded-xl p-4 text-center bg-[#F9F7F2] group-hover:bg-[#EFEBE9] transition-colors">
                  <p class="text-sm text-[#8D6E63] font-medium">
                    클릭하여 사진을 올려주세요 📸
                  </p>
                </div>
              </div>

              <!-- 파일 선택 후 -->
              <div v-else class="flex items-center gap-3 p-3 border border-[#D7CCC8] rounded-xl bg-[#EFEBE9]">
                <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-lg shadow-sm">🖼️</div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-[#5D4037] font-bold truncate">{{ imageFile.name }}</p>
                  <p class="text-xs text-[#8D6E63]">업로드 준비 완료</p>
                </div>
                <button 
                  @click.prevent="removeImage"
                  type="button"
                  class="p-2 text-[#8D6E63] hover:bg-[#D7CCC8] rounded-full transition-colors"
                  title="사진 삭제"
                >
                  <X class="w-5 h-5" />
                </button>
              </div>
            </label>
          </div>

          <div class="mt-10 flex flex-col sm:flex-row justify-end gap-4 pt-6 border-t border-[#EFEBE9]">
            <button
              @click="router.go(-1)"
              class="px-8 py-3 border border-[#D7CCC8] text-sm font-bold rounded-full text-[#8D6E63] hover:bg-[#EFEBE9] transition-colors"
            >
              취소
            </button>
            <button
              @click="handleSubmit"
              :disabled="isSubmitting"
              class="px-10 py-3 bg-[#5D4037] text-white text-sm font-bold rounded-full hover:bg-[#4E342E] disabled:bg-[#BCAAA4] shadow-lg transform hover:-translate-y-1 transition-all"
            >
              {{ isSubmitting ? '굽는 중...' : '등록하기' }}
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