import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/api/axios';

export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  const token = ref(localStorage.getItem('auth_token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user_info')) || null);
  
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
    user.value = newUser;
    localStorage.setItem('user_info', JSON.stringify(newUser));
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

  ///////////////////////////////

  async function signup(userInfo) {
    try {
      // 백엔드가 기대하는 필드 형태로 재구성
      const payload = {
        email: userInfo.email,
        password1: userInfo.password1,
        password2: userInfo.password2,
        // username을 쓰는 설정이면 아래도 포함
        nickname: userInfo.nickname, 
        bread_preferences: userInfo.bread_preferences, // 문자열로 받는다면 그대로

      }

      console.log('📨 Signup payload:', payload)

      const response = await apiClient.post('/accounts/signup/', payload)

      console.log('✅ Signup success:', response.data)

      setToken(response.data.key)
      await fetchUser()
      if (router) router.push('/')
    } catch (error) {
      if (error.response) {
        console.error('❌ Signup 400 data:', error.response.data)
        alert('회원가입에 실패했습니다: ' + JSON.stringify(error.response.data))
      } else {
        console.error('❌ Signup failed:', error)
        alert('회원가입 중 네트워크 오류가 발생했습니다.')
      }
    }
  }

  //////////////////////////////////////////////

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
    setRouter 
  };
});
