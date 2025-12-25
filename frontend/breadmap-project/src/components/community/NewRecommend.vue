<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { X } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const stores = ref([])
const storeQuery = ref('')
const storeId = ref(route.params.storeId || '')
const title = ref('')
const content = ref('')
const rating = ref(5)
const categoryLabel = '빵집 추천'

const imageFile = ref(null)
const fileInputRef = ref(null)
const isSubmitting = ref(false)

onMounted(async () => {
  try { 
    const res = await apiClient.get('/stores/')
    stores.value = res.data 
  } catch (e) { 
    console.error('가게 목록 로드 실패:', e) 
  }
})

const filteredStores = computed(() => {
  const q = storeQuery.value.trim().toLowerCase()
  if (!q) return stores.value.slice(0, 20)
  return stores.value.filter((s) => `${s.name} ${s.address || ''}`.toLowerCase().includes(q)).slice(0, 20)
})

const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (file) {
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

  if (!title.value || !content.value) { alert('제목과 내용을 입력해주세요.'); return }

  // ✅ 빵집 추천 글에는 가게 선택이 필수
  if (!storeId.value) {
    alert('추천할 빵집을 선택해주세요!')
    return
  }

  try {
    isSubmitting.value = true

    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('content', content.value)
    formData.append('category', '빵집 추천')
    formData.append('store', storeId.value)  // ✅ [추가] store ID 전송

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    // Community API 호출
    await apiClient.post('/community/create/', formData, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })

    // ✅ 경험치 획득으로 인한 레벨업 체크를 위해 사용자 정보 갱신
    await authStore.fetchUser()

    alert('추천글이 등록되었습니다! 🥯')
    router.push({ name: 'community' })

  } catch (e) {
    console.error('실패:', e)
    if (e.response?.status === 401) {
      alert('인증 정보가 유효하지 않습니다. 다시 로그인해주세요.')
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
        <h1 class="text-4xl font-serif font-bold text-[#4E342E] mb-2 tracking-wide flex items-center justify-center lg:justify-start gap-2">
          <span class="text-3xl">🥯</span> 빵집 추천하기
        </h1>
        <p class="text-lg text-[#8D6E63] font-medium">나만 알기 아까운 인생 빵집을 공유해주세요!</p>
      </div>

      <div class="bg-white rounded-[40px] shadow-2xl border border-[#D7CCC8] p-8 md:p-12 relative">
        <div class="space-y-6">
          
          <div class="flex items-center gap-2 mb-2">
            <span class="px-4 py-1.5 bg-[#EFEBE9] text-[#5D4037] text-xs font-bold rounded-full border border-[#D7CCC8]">
              {{ categoryLabel }}
            </span>
          </div>

          <!-- 가게 검색 -->
          <div class="space-y-2 relative">
            <span class="text-sm font-bold text-[#5D4037]">가게 선택 <span class="text-[#FF7043]">*</span></span>
            <input
              v-model="storeQuery"
              type="text"
              class="w-full border border-[#D7CCC8] rounded-xl px-4 py-3 text-sm bg-[#FAFAFA] focus:outline-none focus:ring-2 focus:ring-[#8D6E63] placeholder-[#BCAAA4]"
              placeholder="가게 이름을 검색해보세요..."
            />
            <div v-if="storeQuery && filteredStores.length" class="absolute z-20 w-full max-h-48 overflow-y-auto border border-[#D7CCC8] rounded-xl bg-white shadow-lg mt-1 custom-scroll">
              <button
                v-for="store in filteredStores"
                :key="store.id"
                @click="storeId = store.id; storeQuery = store.name"
                class="w-full text-left px-4 py-3 text-sm hover:bg-[#EFEBE9] flex flex-col border-b border-[#F5F5F5] last:border-0"
                :class="{ 'bg-[#EFEBE9]': storeId === store.id }"
              >
                <span class="font-bold text-[#4E342E]">{{ store.name }}</span>
                <span class="text-xs text-[#8D6E63]">{{ store.address }}</span>
              </button>
            </div>
            <p v-if="storeId" class="text-xs text-[#5D4037] font-bold mt-1 flex items-center gap-1">
              ✅ 가게가 선택되었습니다.
            </p>
          </div>

          <!-- 별점 -->
          <div class="space-y-2">
            <span class="text-sm font-bold text-[#5D4037]">평점</span>
            <div class="flex items-center gap-2 bg-[#FAFAFA] p-3 rounded-xl border border-[#D7CCC8] w-fit">
              <button 
                v-for="star in 5" :key="star" @click="rating = star"
                type="button"
                class="text-2xl focus:outline-none transition-transform active:scale-125"
                :class="star <= rating ? 'text-[#FFB74D] drop-shadow-sm' : 'text-[#E0E0E0]'"
              >★</button>
              <span class="text-sm font-bold text-[#5D4037] ml-2">{{ rating }}점</span>
            </div>
          </div>

          <label class="block text-left">
            <span class="text-sm font-bold text-[#5D4037] mb-2 block">제목</span>
            <input v-model="title" type="text" class="w-full border border-[#D7CCC8] rounded-xl px-4 py-3 text-sm bg-[#FAFAFA] focus:outline-none focus:ring-2 focus:ring-[#8D6E63]" placeholder="제목을 입력해주세요" />
          </label>

          <label class="block text-left">
            <span class="text-sm font-bold text-[#5D4037] mb-2 block">내용</span>
            <textarea v-model="content" class="w-full border border-[#D7CCC8] rounded-xl px-4 py-3 text-sm min-h-[200px] bg-[#FAFAFA] focus:outline-none focus:ring-2 focus:ring-[#8D6E63] resize-none" placeholder="추천 이유를 자세히 적어주세요."></textarea>
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

        <div class="mt-10 flex justify-end gap-4 pt-6 border-t border-[#EFEBE9]">
          <button @click="router.go(-1)" class="px-8 py-3 border border-[#D7CCC8] text-sm font-bold rounded-full text-[#8D6E63] hover:bg-[#EFEBE9]">취소</button>
          <button @click="handleSubmit" :disabled="isSubmitting" class="px-10 py-3 bg-[#8D6E63] text-white text-sm font-bold rounded-full hover:bg-[#6D4C41] shadow-lg transform hover:-translate-y-1 transition-all disabled:bg-[#BCAAA4]">
            {{ isSubmitting ? '등록 중...' : '추천하기' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');
.font-serif { font-family: 'Gaegu', cursive; }
.custom-scroll::-webkit-scrollbar { width: 4px; }
.custom-scroll::-webkit-scrollbar-thumb { background-color: #D7CCC8; border-radius: 4px; }
</style>