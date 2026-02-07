<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <!-- Navbar with Glassmorphism and Prism Gradient Border -->
    <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-transparent relative">
      <!-- Prism Gradient Border Bottom -->
      <div class="absolute bottom-0 left-0 w-full h-[2px] bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-blue-500 to-purple-500"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <!-- Prism Logo Effect -->
              <h1 class="text-3xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-red-600 via-purple-600 to-indigo-600 drop-shadow-sm hover:scale-105 transition-transform duration-300 cursor-pointer">
                {{ $t('nav.app_name') }}
              </h1>
            </div>
            <div class="hidden sm:ml-8 sm:flex sm:space-x-8">
              <router-link to="/" class="group inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors duration-200 relative">
                {{ $t('nav.home') }}
                <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-red-400 to-purple-500 transition-all duration-300 group-hover:w-full"></span>
              </router-link>
              <router-link to="/courses" class="group inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors duration-200 relative">
                {{ $t('nav.courses') }}
                 <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-purple-400 to-blue-500 transition-all duration-300 group-hover:w-full"></span>
              </router-link>
              <router-link v-if="isAuthenticated" to="/dashboard" class="group inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors duration-200 relative">
                {{ $t('nav.dashboard') }}
                 <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-400 to-green-500 transition-all duration-300 group-hover:w-full"></span>
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-6">
             <!-- Language Switcher with Hover Effect -->
             <div class="relative">
                 <select v-model="currentLocale" @change="changeLocale" class="appearance-none bg-gray-100 hover:bg-gray-200 border-none rounded-full py-1.5 pl-4 pr-8 text-sm focus:ring-2 focus:ring-purple-500 transition-colors cursor-pointer">
                    <option value="pt-BR">🇧🇷 PT-BR</option>
                    <option value="en">🇺🇸 EN</option>
                 </select>
                 <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                 </div>
             </div>

             <template v-if="!isAuthenticated">
                <router-link to="/login" class="text-gray-500 hover:text-gray-900 text-sm font-medium transition-colors duration-200">
                  {{ $t('nav.login') }}
                </router-link>
                <router-link to="/register" class="relative inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 transform transition-all hover:scale-105 active:scale-95">
                  <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md group-hover:bg-opacity-0 text-gray-900 group-hover:text-white">
                      {{ $t('nav.register') }}
                  </span>
                </router-link>
             </template>
             <template v-else>
                <router-link to="/profile" class="text-gray-700 mr-2 text-sm font-medium hidden md:block hover:text-purple-600 transition-colors cursor-pointer">
                    {{ $t('nav.welcome') }}
                </router-link>
                <button @click="logout" class="text-gray-500 hover:text-red-600 text-sm font-medium transition-colors duration-200">
                  {{ $t('nav.logout') }}
                </button>
             </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="relative">
       <!-- Background decoration (Subtle Prism Light) -->
       <div class="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-purple-50 to-transparent -z-10"></div>
       <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 relative z-0">
         <router-view></router-view>
       </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

// Simple auth check mock - in real app use Pinia store
const isAuthenticated = computed(() => !!localStorage.getItem('token'));
const router = useRouter();
const { locale } = useI18n();
const currentLocale = ref(locale.value);

const logout = () => {
  localStorage.removeItem('token');
  window.location.reload(); // Simple reload to clear state
};

const changeLocale = () => {
  locale.value = currentLocale.value;
};
</script>
