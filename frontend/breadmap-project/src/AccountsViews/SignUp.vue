<template>
  <div class="min-h-screen bg-cream-100 flex items-center justify-center p-4">
    <div class="w-full max-w-4xl bg-white rounded-2xl shadow-soft overflow-hidden flex flex-col md:flex-row">
      
      <!-- Image Section (only for Step 1) -->
      <div v-if="step === 1" class="w-full md:w-1/2 flex items-center justify-center p-8 bg-cream-50">
        <img src="@/assets/images/식빵.png" alt="A slice of toast" class="max-w-full h-auto object-contain" style="max-height: 400px;">
      </div>

      <!-- Form Section -->
      <div class="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center relative">
        <img src="https://i.imgur.com/JzJ4JzL.png" alt="A croissant" class="absolute top-4 right-4 w-20">
        
        <!-- Step 1: User Info -->
        <div v-if="step === 1">
          <p class="text-teal-800 font-semibold">STEP 1</p>
          <h1 class="text-4xl font-bold text-brown-text font-serif mb-2">환영합니다!</h1>
          <p class="text-gray-600 mb-8">지금 가입하고<br>나만의 빵지순례 지도를 만드세요.</p>
          
          <form @submit.prevent="nextStep" class="space-y-4">
            <input type="email" v-model="form.email" placeholder="Email" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="text" v-model="form.nickname" placeholder="Nickname" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="password" v-model="form.password1" placeholder="Password" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="password" v-model="form.password2" placeholder="Confirm Password" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <button type="submit" class="w-full py-3 font-semibold text-white transition-transform duration-200 transform rounded-lg bg-teal-800 hover:bg-teal-900 active:scale-95">Next</button>
          </form>

          <div class="text-center mt-4 text-sm">
            <p class="text-gray-500">이미 계정이 있으신가요? <router-link to="/login" class="font-semibold text-teal-800 hover:underline">로그인 하러가기</router-link></p>
          </div>
        </div>

        <!-- Step 2: Bread Preferences -->
        <div v-if="step === 2">
          <p class="text-teal-800 font-semibold">STEP 2/2</p>
          <h1 class="text-4xl font-bold text-brown-text font-serif mb-2">{{ form.nickname || 'USER' }}님의<br>빵 취향을 알려주세요</h1>
          <p class="text-gray-600 mb-8">좋아하는 종류를 모두 선택해주세요.</p>
          
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-8">
            <button v-for="pref in preferences" :key="pref.name" @click="togglePreference(pref.name)"
                    :class="['p-4 border rounded-lg flex flex-col items-center justify-center transition-all', form.bread_preferences.includes(pref.name) ? 'bg-teal-800 text-white border-teal-800' : 'bg-cream-50 border-cream-200 hover:border-teal-800']">
              <span class="text-3xl mb-2">{{ pref.emoji }}</span>
              <span class="font-semibold">{{ pref.name }}</span>
            </button>
          </div>

          <div class="flex gap-4">
            <button @click="step = 1" class="w-1/3 py-3 font-semibold text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">Back</button>
            <button @click="handleSignup" class="w-2/3 py-3 font-semibold text-white transition-transform duration-200 transform rounded-lg bg-teal-800 hover:bg-teal-900 active:scale-95">빵지순례 시작하기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router';

const step = ref(1);
const form = reactive({
  email: '',
  nickname: '',
  password1: '',
  password2: '',
  bread_preferences: [],
});

const preferences = ref([
  { name: '담백/고소', emoji: '🥖' },
  { name: '달콤한', emoji: '🥐' },
  { name: '부드러운', emoji: '🍞' },
  { name: '바삭/하드', emoji: '🥨' },
  { name: '디저트류', emoji: '🍰' },
  { name: '조리빵', emoji: '🌭' },
]);

const authStore = useAuthStore();

const nextStep = () => {
  if (form.password1 !== form.password2) {
    alert('Passwords do not match!');
    return;
  }
  if (form.email && form.nickname && form.password1) {
    step.value = 2;
  } else {
    alert('Please fill out all fields in Step 1.');
  }
};

const togglePreference = (prefName) => {
  const index = form.bread_preferences.indexOf(prefName);
  if (index > -1) {
    form.bread_preferences.splice(index, 1);
  } else {
    form.bread_preferences.push(prefName);
  }
};

const handleSignup = () => {
  authStore.signup({
    email: form.email,
    nickname: form.nickname,
    password1: form.password1, // 키 이름을 'password'에서 'password1'으로 변경
    password2: form.password2,
    bread_preferences: form.bread_preferences.join(','),
  });
};
</script>