import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/api/axios';

export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  const token = ref(localStorage.getItem('auth_token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user_info')) || null);

  // ✅ [추가] 레벨업 상태 관리
  const levelUpInfo = ref(null);
  const showLevelUpModal = ref(false);

  // --- Router ---
  // 컴포넌트가 아닌 곳에서 router를 사용하기 위해 setup 스코프 밖에서 선언
  let router;
  // 이 스토어가 사용될 때 router 인스턴스를 주입받기 위한 함수
  const setRouter = (r) => router = r;

  // --- Getters ---
  const isAuthenticated = computed(() => !!token.value);
  const currentUser = computed(() => user.value);

  // --- Actions ---
  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem('auth_token', newToken);
  }

  function setUser(newUser) {
    // ✅ [추가] 레벨업 감지
    const oldLevel = user.value?.level;
    const newLevel = newUser?.level;

    if (oldLevel && newLevel && newLevel > oldLevel) {
      // 레벨업 발생!
      triggerLevelUp(oldLevel, newLevel, newUser);
    }

    user.value = newUser;
    localStorage.setItem('user_info', JSON.stringify(newUser));
  }

  // ✅ [추가] 레벨업 트리거 함수
  function triggerLevelUp(oldLevel, newLevel, userData) {
    levelUpInfo.value = {
      oldLevel,
      newLevel,
      character: getLevelCharacter(newLevel),
      userData
    };
    showLevelUpModal.value = true;
  }

  // ✅ [추가] 레벨별 캐릭터 정보
  function getLevelCharacter(level) {
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
      10: { name: '황금밀 유니콘', icon: '🦄', color: 'text-purple-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235359.png' }
    };
    return LEVEL_CONFIG[level] || LEVEL_CONFIG[1];
  }

  // ✅ [추가] 레벨업 모달 닫기
  function closeLevelUpModal() {
    showLevelUpModal.value = false;
    levelUpInfo.value = null;
  }

  function clearAuth() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
  }

  async function login(credentials) {
    try {
      const response = await apiClient.post('/accounts/login/', credentials);
      setToken(response.data.key);
      await fetchUser();
      if (router) router.push('/');
    } catch (error) {
      console.error('Login failed:', error);
      alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.');
    }
  }

  async function signup(userInfo) {
    try {
      const response = await apiClient.post('/accounts/signup/', userInfo);
      setToken(response.data.key);
      await fetchUser();
      if (router) router.push('/');
    } catch (error) {
      console.error('Signup failed:', error);
      alert('회원가입에 실패했습니다. 입력 정보를 확인하세요.');
    }
  }

  async function logout() {
    if (!token.value) return;
    try {
      await apiClient.post('/accounts/logout/');
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      clearAuth();
      if (router) router.push('/login');
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      const response = await apiClient.get('/accounts/user/');
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      clearAuth(); // 토큰이 유효하지 않을 수 있으므로 인증 정보 초기화
    }
  }

  // 앱 시작 시 사용자 정보 가져오기
  if (token.value) {
    fetchUser();
  }

  return {
    token,
    user,
    isAuthenticated,
    currentUser,
    login,
    logout,
    signup,
    fetchUser,
    setRouter,
    // ✅ [추가] 레벨업 관련
    levelUpInfo,
    showLevelUpModal,
    closeLevelUpModal
  };
});
