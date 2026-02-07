<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">{{ $t('dashboard.title') }}</h3>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">{{ $t('dashboard.my_courses') }}</p>
    </div>
    <div class="border-t border-gray-200">
      <div v-if="enrollments.length === 0" class="p-6 text-center text-gray-500">
        {{ $t('dashboard.no_enrollments') }}
        <div class="mt-4">
            <router-link to="/courses" class="text-indigo-600 hover:text-indigo-900 font-medium">
                {{ $t('dashboard.browse_courses') }} &rarr;
            </router-link>
        </div>
      </div>
      <ul v-else role="list" class="divide-y divide-gray-200">
        <li v-for="enrollment in enrollments" :key="enrollment.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50 transition duration-150 ease-in-out">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
                <h4 class="text-lg font-bold text-indigo-600 truncate">{{ enrollment.course_title }}</h4>
                <p class="text-sm text-gray-500 truncate">{{ enrollment.course_description }}</p>
                <div class="mt-2">
                    <div class="flex items-center text-sm text-gray-500">
                        <span class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400">
                             <!-- Clock Icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                            </svg>
                        </span>
                        {{ $t('dashboard.last_accessed') }}: {{ new Date(enrollment.enrolled_at).toLocaleDateString() }}
                    </div>
                </div>
            </div>
            <div class="ml-4 flex-shrink-0 flex flex-col items-end">
                 <div class="text-sm font-medium text-gray-900 mb-1">{{ enrollment.progress }}%</div>
                 <div class="w-24 bg-gray-200 rounded-full h-2 mb-2">
                    <div class="bg-gradient-to-r from-green-400 to-blue-500 h-2 rounded-full" :style="{ width: enrollment.progress + '%' }"></div>
                 </div>
                 <button class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transform hover:scale-105 transition-all duration-200">
                     {{ $t('dashboard.continue') }}
                 </button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const enrollments = ref([]);

const fetchEnrollments = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return;
    
    const response = await axios.get('http://localhost:8000/api/enrollments/', {
        headers: { 'Authorization': `Token ${token}` }
    });
    enrollments.value = response.data;
  } catch (err) {
    console.error('Error fetching enrollments:', err);
  }
};

onMounted(fetchEnrollments);
</script>
