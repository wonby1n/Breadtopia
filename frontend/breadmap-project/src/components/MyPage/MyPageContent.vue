<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { Award, Settings, Receipt, BookOpen, Bookmark } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
// 👇 컴포넌트 import
import BreadPassport from './BreadPassport.vue';
import BakeryScrapbook from './BakeryScrapBook.vue';
import BadgePinBoard from './BadgePinBoard.vue';
import MyReviewsSection from './MyReviewsSection.vue';
import MyPostsSection from './MyPostsSection.vue';

const authStore = useAuthStore();
const isLoading = ref(true);
const userInfo = ref(null);
const router = useRouter();

// 탭 상태 관리
const activeTab = ref('passport');

const showFollowModal = ref(false);
const followModalType = ref('followers');
const followList = ref([]);

// 1️⃣ 10단계 레벨 및 캐릭터 설정
const LEVEL_CONFIG = {
  1: { name: '아기빵쥐', icon: '🐭', color: 'text-gray-400', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  2: { name: '식빵햄찌', icon: '🐹', color: 'text-orange-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  3: { name: '호빵토끼', icon: '🐰', color: 'text-pink-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235372.png' },
  4: { name: '모닝코기', icon: '🐶', color: 'text-yellow-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235415.png' },
  5: { name: '크루아상여우', icon: '🦊', color: 'text-orange-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235368.png' },
  6: { name: '브리오슈곰', icon: '🐻', color: 'text-brown-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235388.png' },
  7: { name: '사워도우울프', icon: '🐺', color: 'text-gray-600', img: 'https://cdn-icons-png.flaticon.com/512/235/235356.png' },
  8: { name: '초코표범', icon: '🐆', color: 'text-yellow-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235377.png' },
  9: { name: '바게트호크', icon: '🦅', color: 'text-teal-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235386.png' },
  10: { name: '황금밀 유니콘', icon: '🦄', color: 'text-purple-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235359.png' },
};

const currentLevelInfo = computed(() => {
  if (!userInfo.value) return LEVEL_CONFIG[1];
  return LEVEL_CONFIG[userInfo.value.level] || LEVEL_CONFIG[1];
});

const progressWidth = computed(() => {
  if (!userInfo.value) return '0%';
  const percent = (userInfo.value.exp / userInfo.value.next_exp) * 100; 
  return `${Math.min(percent, 100)}%`;
});

const fetchUserProfile = async () => {
  try {
    const token = authStore.token;
    if (!token) {
      isLoading.value = false;
      return;
    }

    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: { Authorization: `Token ${token}` }
    });

    const data = response.data;

    // ✨ 수정됨: 더미 데이터 로직 제거하고 실제 데이터만 할당
    const bookmarkedStores = data.bookmarked_stores || [];
    const badges = data.badges || [];
    const tasteStats = data.taste_stats || {};

    // 방문 데이터 가공
    const visitedStores = (data.visited_stores || []).map(store => ({
      id: store.id,
      name: store.name,
      category: store.category || '빵집',
      location: store.address || '',
      date: store.visited_date || new Date().toISOString().split('T')[0] // 실제 방문 날짜가 있다면 사용
    }));

    userInfo.value = {
      nickname: data.nickname || data.username,
      level: data.level || 1,
      level_title: LEVEL_CONFIG[data.level || 1].name,
      exp: data.exp || 0,
      next_exp: data.max_exp || 100,
      profile_image_url: data.profile_image_url ? `http://127.0.0.1:8000${data.profile_image_url}` : null,
      character_type: data.character_type || 'hamster',
      follower_count: data.follower_count || 0,
      following_count: data.following_count || 0,
      review_count: data.review_count || 0,
      post_count: data.post_count || 0,
      badges: badges,
      visited_stores: visitedStores,
      bookmarked_stores: bookmarkedStores,
      taste_stats: tasteStats,
      user_reviews: data.user_reviews || [],
      user_posts: data.user_posts || [],
      date_joined: data.date_joined || new Date().toISOString().split('T')[0]
    };
    isLoading.value = false;

  } catch (error) {
    console.error('프로필 로드 실패:', error);
    isLoading.value = false;
  }
};

const characterImages = {
  hamster: 'https://cdn-icons-png.flaticon.com/512/235/235394.png',
  bear: 'https://cdn-icons-png.flaticon.com/512/235/235388.png',
  lion: 'https://cdn-icons-png.flaticon.com/512/235/235352.png'
};

const getProfileImage = computed(() => {
  if (!userInfo.value) return LEVEL_CONFIG[1].img;
  if (userInfo.value.profile_image_url) return userInfo.value.profile_image_url;
  if (userInfo.value.character_type && characterImages[userInfo.value.character_type]) {
    return characterImages[userInfo.value.character_type];
  }
  return currentLevelInfo.value.img;
});

const handleImageError = (event) => {
  event.target.src = currentLevelInfo.value.img;
};

const openFollowModal = async (type) => {
  followModalType.value = type;
  showFollowModal.value = true;

  try {
    const token = authStore.token;
    if (!token) return;

    let response;
    if (type === 'followers') {
      response = await axios.get('http://127.0.0.1:8000/accounts/followers/', {
        headers: { Authorization: `Token ${token}` }
      });
      followList.value = response.data.followers || [];
    } else if (type === 'following') {
      response = await axios.get('http://127.0.0.1:8000/accounts/following/', {
        headers: { Authorization: `Token ${token}` }
      });
      followList.value = response.data.following || [];
    } else if (type === 'reviews') {
      response = await axios.get('http://127.0.0.1:8000/reviews/my/', {
        headers: { Authorization: `Token ${token}` }
      });
      followList.value = response.data;
    } else if (type === 'posts') {
      // API가 따로 없다면 userInfo에 있는 데이터 사용
      followList.value = userInfo.value?.user_posts || [];
    }
  } catch (error) {
    console.error(`${type} 데이터 로드 실패:`, error);
    followList.value = [];
  }
};

const closeFollowModal = () => {
  showFollowModal.value = false;
  followList.value = [];
};

const receiptEdgeStyle = {
    background: 'linear-gradient(135deg, transparent 5px, white 5px) top left, linear-gradient(225deg, transparent 5px, white 5px) top right',
    backgroundSize: '10px 10px',
    backgroundRepeat: 'repeat-x',
    height: '10px',
    width: '100%',
    position: 'absolute',
    bottom: '-10px',
    left: '0'
};

// 북마크 변경 이벤트 리스너
const handleBookmarkChanged = () => {
  // 북마크만 다시 조회
  fetchUserProfile();
};

onMounted(() => {
  fetchUserProfile();
  // 북마크 변경 이벤트 감지
  window.addEventListener('bookmark-changed', handleBookmarkChanged);
});

onUnmounted(() => {
  window.removeEventListener('bookmark-changed', handleBookmarkChanged);
});
</script>

<template>
  <div class="bg-[#F9F7F2] min-h-screen pb-20 font-sans">
    
    <!-- 로딩 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center h-screen">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-[#AED581] border-t-transparent"></div>
      <p class="mt-4 text-[#5D4037] font-bold animate-pulse font-serif">빵 굽는 중... 🥐</p>
    </div>

    <!-- 데이터 로드 완료 -->
    <div v-else-if="userInfo">
      
      <!-- 1. 프로필 헤더 -->
      <div class="relative pt-12 pb-20 px-6 rounded-b-[50px] shadow-xl overflow-hidden z-10 bg-gradient-to-b from-[#F1F8E9] to-[#DCEDC8]">
        
        <!-- 배경 효과 -->
        <div class="absolute top-[-20%] left-[-10%] w-72 h-72 bg-lime-200/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
        <div class="absolute top-[-20%] right-[-10%] w-72 h-72 bg-green-200/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-[-20%] left-[20%] w-72 h-72 bg-yellow-100/60 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
        <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/cream-paper.png')]"></div>

        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8 relative z-10">
          
          <!-- 캐릭터/프로필 이미지 -->
          <div class="relative group cursor-pointer transition-transform hover:scale-105 duration-300 shrink-0">
            <div class="w-36 h-36 bg-white rounded-full border-[6px] border-white shadow-xl flex items-center justify-center overflow-hidden relative z-10">
              <img :src="getProfileImage" :class="userInfo.profile_image_url ? 'w-full h-full object-cover' : 'w-24 h-24 object-contain drop-shadow-lg'" @error="handleImageError">
            </div>
            <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 bg-[#8BC34A] text-white font-bold px-4 py-1.5 rounded-full shadow-lg whitespace-nowrap z-20 flex items-center gap-1 text-sm font-serif border border-white/50">
              <span class="text-xs opacity-90">Lv.{{ userInfo.level }}</span>
              <span>{{ currentLevelInfo.name }}</span>
            </div>
          </div>

          <!-- 정보 (오른쪽) -->
          <div class="flex-1 text-center md:text-left w-full">
            <div class="flex flex-col md:flex-row md:items-end gap-3 mb-3 justify-center md:justify-start">
              <h2 class="text-3xl font-extrabold tracking-tight text-[#4E342E] font-serif">{{ userInfo.nickname }}</h2>
              <span class="text-2xl animate-bounce">{{ currentLevelInfo.icon }}</span>
            </div>

            <!-- 경험치 바 -->
            <div class="relative mb-2 group max-w-md mx-auto md:mx-0">
              <div class="w-full bg-white/60 h-5 rounded-full overflow-hidden backdrop-blur-sm border border-white/40 shadow-inner">
                <div class="bg-gradient-to-r from-[#DCE775] to-[#8BC34A] h-full rounded-full transition-all duration-1000 relative bg-[length:200%_100%] animate-[shimmer_2s_infinite]" 
                     :style="{ width: progressWidth }">
                </div>
              </div>
              <div class="absolute top-0 w-full text-center text-[10px] font-bold text-[#558B2F] leading-5 drop-shadow-sm">
                {{ userInfo.exp }} / {{ userInfo.next_exp }} EXP
              </div>
            </div>
            
            <p class="text-xs text-[#795548] text-center md:text-left mb-5">
              "{{ currentLevelInfo.name }}" 단계입니다. 맛있는 빵을 찾아 떠나보세요! 🚀
            </p>

            <!-- 스탯 요약 -->
            <div class="flex justify-center md:justify-start gap-4 p-3 bg-white/40 rounded-2xl backdrop-blur-md border border-white/50 shadow-sm inline-flex flex-wrap">
              <div @click="openFollowModal('followers')" class="text-center cursor-pointer hover:text-[#558B2F] transition-colors px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.follower_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Followers</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div @click="openFollowModal('following')" class="text-center cursor-pointer hover:text-[#558B2F] transition-colors px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.following_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Following</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div @click="openFollowModal('reviews')" class="text-center cursor-pointer hover:text-[#558B2F] transition-colors px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.review_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Reviews</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div @click="openFollowModal('posts')" class="text-center cursor-pointer hover:text-[#558B2F] transition-colors px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.post_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Posts</p>
              </div>
            </div>
          </div>
          <!-- 설정 버튼 -->
          <button @click="router.push({ name: 'editprofile' })" class="absolute top-0 right-0 p-2 text-[#8D6E63] hover:text-[#558B2F] hover:bg-white/30 rounded-full transition-all">
            <Settings class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- 2. 탭 메뉴 -->
      <div class="max-w-5xl mx-auto px-4 -mt-10 relative z-20">
        <div class="bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/60 p-1.5 flex justify-between md:justify-start gap-2 overflow-x-auto hide-scrollbar">
          
          <button @click="activeTab = 'passport'" 
                  :class="['flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-300 font-bold text-sm whitespace-nowrap flex-1 md:flex-none justify-center', 
                           activeTab === 'passport' ? 'bg-[#8BC34A] text-white shadow-md' : 'text-gray-500 hover:bg-[#F1F8E9] hover:text-[#8BC34A]']">
            <BookOpen class="w-4 h-4" /> 내 여권
          </button>
          
          <button @click="activeTab = 'taste'" 
                  :class="['flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-300 font-bold text-sm whitespace-nowrap flex-1 md:flex-none justify-center', 
                           activeTab === 'taste' ? 'bg-[#8BC34A] text-white shadow-md' : 'text-gray-500 hover:bg-[#F1F8E9] hover:text-[#8BC34A]']">
            <Receipt class="w-4 h-4" /> 취향 분석
          </button>
          
          <button @click="activeTab = 'badge'" 
                  :class="['flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-300 font-bold text-sm whitespace-nowrap flex-1 md:flex-none justify-center', 
                           activeTab === 'badge' ? 'bg-[#8BC34A] text-white shadow-md' : 'text-gray-500 hover:bg-[#F1F8E9] hover:text-[#8BC34A]']">
            <Award class="w-4 h-4" /> 뱃지 보관함
          </button>
          
          <button @click="activeTab = 'scrap'" 
                  :class="['flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-300 font-bold text-sm whitespace-nowrap flex-1 md:flex-none justify-center', 
                           activeTab === 'scrap' ? 'bg-[#8BC34A] text-white shadow-md' : 'text-gray-500 hover:bg-[#F1F8E9] hover:text-[#8BC34A]']">
            <Bookmark class="w-4 h-4" /> 빵킷리스트
          </button>
        </div>
      </div>

      <!-- 메인 컨텐츠 영역 -->
      <div class="max-w-5xl mx-auto px-4 sm:px-6 pt-8 pb-20">
        <Transition name="fade" mode="out-in">
          
          <!-- 1. 여권 탭 -->
          <div v-if="activeTab === 'passport'" key="passport" class="space-y-6">
             <div class="bg-white rounded-3xl p-6 md:p-10 shadow-xl border border-[#F0EBE0] min-h-[500px]">
               <BreadPassport 
                 :visited-stores="userInfo.visited_stores" 
                 :date-joined="userInfo.date_joined"
               />
               <p class="text-center text-[#8D6E63] text-sm mt-6">
                 방문한 빵집에 스탬프가 찍힙니다. 여행을 계속하세요! ✈️
               </p>
             </div>
          </div>

          <!-- 2. 취향 분석 탭 -->
          <div v-else-if="activeTab === 'taste'" key="taste" class="flex justify-center items-start min-h-[500px]">
             <div class="w-full max-w-md">
                <div class="relative bg-white w-full shadow-2xl relative p-8 font-mono text-sm text-gray-700 transform rotate-1 transition-transform hover:rotate-0 duration-500 origin-top">
                  <div class="absolute top-3 left-1/2 -translate-x-1/2 w-4 h-4 bg-[#F9F7F2] rounded-full shadow-inner border border-gray-200"></div>
                  <div class="text-center border-b-2 border-dashed border-gray-300 pb-6 mb-6">
                    <Receipt class="w-10 h-10 mx-auto text-gray-400 mb-3" />
                    <h3 class="text-2xl font-bold tracking-widest text-black">BREAD RECEIPT</h3>
                    <p class="text-xs text-gray-500 mt-2 tracking-wide">{{ new Date().toLocaleDateString() }} • {{ userInfo.nickname }}</p>
                  </div>
                  <div v-if="Object.keys(userInfo.taste_stats).length > 0" class="space-y-4 mb-8">
                    <div class="flex justify-between text-xs text-gray-500 uppercase tracking-wider border-b border-gray-200 pb-2">
                      <span>Bread Menu</span>
                      <span>Times</span>
                    </div>
                    <div v-for="(count, menu) in userInfo.taste_stats" :key="menu" class="flex justify-between items-end group">
                      <span class="font-bold text-lg text-gray-800 group-hover:text-[#8BC34A] transition-colors">{{ menu }}</span>
                      <span class="text-gray-300 border-b-2 border-dotted border-gray-200 flex-1 mx-3 mb-1"></span>
                      <span class="font-bold text-lg">{{ count }}x</span>
                    </div>
                  </div>
                  <div v-else class="py-12 text-center text-gray-400">
                    <p>아직 먹은 빵이 없어요 🥺</p>
                    <p class="text-xs mt-2">리뷰를 작성하면 취향 분석이 표시됩니다!</p>
                  </div>
                  <div class="border-t-2 border-dashed border-gray-300 pt-6 text-center">
                    <div v-if="Object.keys(userInfo.taste_stats).length > 0" class="mb-6 relative inline-block">
                        <p class="text-[10px] text-gray-500 mb-2 uppercase tracking-widest">🏆 Most Loved</p>
                        <p class="text-3xl font-black text-red-500 border-[3px] border-red-500 px-6 py-2 rounded-lg transform -rotate-3 opacity-80" style="font-family: 'Gaegu', cursive;">
                          {{ Object.keys(userInfo.taste_stats).reduce((a, b) => userInfo.taste_stats[a] > userInfo.taste_stats[b] ? a : b) }}
                        </p>
                    </div>
                    <div class="h-14 w-4/5 mx-auto bg-[url('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/UPC-A-036000291452.png/640px-UPC-A-036000291452.png')] bg-cover opacity-70 grayscale mb-2"></div>
                    <p class="text-[10px] tracking-[0.5em] text-center">THANK YOU</p>
                  </div>
                  <div :style="receiptEdgeStyle"></div>
                </div>
             </div>
          </div>

          <!-- 3. 뱃지 보관함 탭 -->
          <div v-else-if="activeTab === 'badge'" key="badge" class="space-y-6">
             <div class="bg-[#2C3E50] rounded-3xl p-6 md:p-10 shadow-2xl min-h-[500px] border border-[#34495E]">
                <BadgePinBoard 
                   :badges="userInfo.badges" 
                />
                <p class="text-center text-gray-500 text-sm mt-8">
                   다양한 활동으로 뱃지를 모아 명예의 전당을 채워보세요. 🏆
                </p>
             </div>
          </div>

          <!-- 4. 빵킷리스트 탭 -->
          <div v-else-if="activeTab === 'scrap'" key="scrap" class="h-[600px]">
             <BakeryScrapbook 
               :bookmarked-stores="userInfo.bookmarked_stores" 
             />
          </div>

        </Transition>
      </div>
    </div>

    <!-- 모달 -->
    <Transition name="modal">
      <div v-if="showFollowModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" @click.self="closeFollowModal">
        <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden flex flex-col">
          <div class="bg-[#8BC34A] text-white p-5 flex items-center justify-between shrink-0">
            <h3 class="text-lg font-bold">
              {{ followModalType === 'followers' ? '나를 따르는 빵순이들' :
                 followModalType === 'following' ? '내가 팔로우한 빵순이들' :
                 followModalType === 'reviews' ? '내가 작성한 리뷰' : '내가 작성한 게시글' }}
            </h3>
            <button @click="closeFollowModal" class="text-white/80 hover:text-white transition-colors">✕</button>
          </div>
          <div class="p-6 overflow-y-auto">
            <div v-if="followModalType === 'followers' || followModalType === 'following'">
              <div v-if="followList.length === 0" class="text-center text-gray-400 py-8">
                <p class="text-4xl mb-4">🥐</p>
                <p>{{ followModalType === 'followers' ? '아직 팔로워가 없습니다' : '아직 팔로우한 사용자가 없습니다' }}</p>
              </div>
              <div v-else class="space-y-3">
                <div
                  v-for="user in followList"
                  :key="user.id"
                  class="flex items-center gap-4 p-4 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors"
                >
                  <div class="w-12 h-12 bg-gradient-to-br from-lime-200 to-green-300 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {{ user.nickname ? user.nickname[0].toUpperCase() : user.username[0].toUpperCase() }}
                  </div>
                  <div class="flex-1">
                    <p class="font-bold text-gray-800">{{ user.nickname || user.username }}</p>
                    <p class="text-xs text-gray-500">Lv.{{ user.level || 1 }} {{ user.level_title || '아기빵쥐' }}</p>
                  </div>
                    <button
                    class="px-4 py-2 bg-[#8BC34A] text-white rounded-full text-sm font-bold hover:bg-[#7CB342] transition-colors"
                    @click="router.push({ name: 'userProfile', params: { userId: user.id } })"> 
                    프로필 보기
                  </button>
                </div>
              </div>
            </div>
            <MyReviewsSection v-else-if="followModalType === 'reviews'" :reviews="followList" />
            <MyPostsSection v-else-if="followModalType === 'posts'" :posts="followList" />
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Gaegu:wght@400;700&display=swap');
div { font-family: 'Noto Sans KR', sans-serif; }
h2, .font-serif { font-family: 'Gaegu', cursive; }
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .bg-white, .modal-leave-active .bg-white { transition: transform 0.2s ease; }
.modal-enter-from .bg-white, .modal-leave-to .bg-white { transform: scale(0.95); }

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>