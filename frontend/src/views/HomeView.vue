<template>
  <div class="bg-white">
    <!-- Hero Section with Prism Dispersion Background -->
    <div class="relative bg-black overflow-hidden">
      <!-- Prism Background Effect -->
      <div class="absolute inset-0 opacity-80">
          <div class="absolute inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900"></div>
          <!-- Light Beams -->
          <div class="absolute top-0 left-1/4 w-96 h-full bg-gradient-to-b from-white/10 to-transparent transform -skew-x-12 blur-3xl"></div>
          <div class="absolute bottom-0 right-1/4 w-96 h-full bg-gradient-to-t from-purple-500/20 to-transparent transform skew-x-12 blur-3xl"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8 text-center">
        <h1 class="text-5xl font-extrabold tracking-tight text-white sm:text-6xl lg:text-7xl">
          <span class="block bg-clip-text text-transparent bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-blue-500 to-purple-500 animate-pulse">
             {{ $t('home.hero_title') }}
          </span>
        </h1>
        <p class="mt-6 text-xl text-gray-300 max-w-3xl mx-auto">
          {{ $t('home.hero_subtitle') }}
        </p>
        <div class="mt-10 max-w-sm mx-auto sm:max-w-none sm:flex sm:justify-center">
          <div class="space-y-4 sm:space-y-0 sm:inline-grid sm:grid-cols-2 sm:gap-5">
            <router-link to="/courses" class="flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-black bg-white hover:bg-gray-100 hover:scale-105 transition-transform duration-200 shadow-[0_0_15px_rgba(255,255,255,0.5)]">
              {{ $t('home.start_now') }}
            </router-link>
            <router-link to="/login" class="flex items-center justify-center px-8 py-3 border border-white text-base font-medium rounded-md text-white bg-transparent hover:bg-white/10 hover:scale-105 transition-all duration-200 backdrop-blur-sm">
              {{ $t('home.login_button') }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Feature Section -->
    <div class="py-16 bg-gray-50 overflow-hidden lg:py-24 relative">
       <!-- Subtle colored background blobs -->
       <div class="absolute top-0 left-0 w-64 h-64 bg-red-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
       <div class="absolute top-0 right-0 w-64 h-64 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
       <div class="absolute -bottom-8 left-20 w-64 h-64 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>

      <div class="relative max-w-xl mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl">
        <div class="relative text-center">
          <h2 class="text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600">
            {{ $t('home.why_study') }}
          </h2>
          <p class="mt-4 max-w-3xl mx-auto text-xl text-gray-500">
            {{ $t('home.why_study_desc') }}
          </p>
        </div>

        <div class="relative mt-12 lg:mt-24 lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
          <div class="relative">
            <h3 class="text-2xl font-extrabold text-gray-900 tracking-tight sm:text-3xl">
              {{ $t('home.inclusive_edu') }}
            </h3>
            <p class="mt-3 text-lg text-gray-500">
              {{ $t('home.inclusive_edu_desc') }}
            </p>

            <dl class="mt-10 space-y-10">
              <div class="relative group">
                <dt>
                  <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-br from-pink-500 to-orange-400 text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <!-- Icon placeholder -->
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ $t('home.specialized_content') }}</p>
                </dt>
                <dd class="mt-2 ml-16 text-base text-gray-500">
                  {{ $t('home.specialized_content_desc') }}
                </dd>
              </div>

              <div class="relative group">
                <dt>
                  <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-br from-purple-500 to-indigo-500 text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <!-- Icon placeholder -->
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ $t('home.community') }}</p>
                </dt>
                <dd class="mt-2 ml-16 text-base text-gray-500">
                  {{ $t('home.community_desc') }}
                </dd>
              </div>
            </dl>
          </div>

          <div class="mt-10 -mx-4 relative lg:mt-0" aria-hidden="true">
             <!-- Prism Graphic Placeholder -->
             <div class="relative mx-auto rounded-xl shadow-2xl overflow-hidden bg-white p-8 h-96 flex items-center justify-center border border-gray-100 transform rotate-1 hover:rotate-0 transition-transform duration-500">
                 <div class="absolute inset-0 bg-gradient-to-tr from-gray-50 to-gray-100 z-0"></div>
                 <div class="text-center relative z-10">
                    <!-- Simple Prism SVG representation -->
                    <svg class="mx-auto h-40 w-40 drop-shadow-lg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M50 15L85 85H15L50 15Z" fill="url(#prism-gradient)" stroke="black" stroke-width="0.5"/>
                        <!-- Light beam in -->
                        <path d="M0 40L35 55" stroke="white" stroke-width="2" stroke-opacity="0.8"/>
                        <!-- Light beam out (Rainbow) -->
                        <path d="M65 55L100 30" stroke="#FF0000" stroke-width="2" />
                        <path d="M65 55L100 35" stroke="#FFA500" stroke-width="2" />
                        <path d="M65 55L100 40" stroke="#FFFF00" stroke-width="2" />
                        <path d="M65 55L100 45" stroke="#008000" stroke-width="2" />
                        <path d="M65 55L100 50" stroke="#0000FF" stroke-width="2" />
                        <path d="M65 55L100 55" stroke="#4B0082" stroke-width="2" />
                        <path d="M65 55L100 60" stroke="#EE82EE" stroke-width="2" />
                        
                        <defs>
                            <linearGradient id="prism-gradient" x1="50" y1="15" x2="50" y2="85" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#E0F2FE" stop-opacity="0.8"/>
                                <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.4"/>
                            </linearGradient>
                        </defs>
                    </svg>
                    <p class="mt-6 text-gray-800 font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
                        {{ $t('home.respect_diversity') }}
                    </p>
                 </div>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-gray-900 relative overflow-hidden">
      <!-- Gradient overlay -->
      <div class="absolute inset-0 bg-gradient-to-r from-purple-900 to-blue-900 opacity-90"></div>
      
      <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8 relative z-10">
        <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
          <span class="block">{{ $t('home.ready_to_learn') }}</span>
          <span class="block bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">{{ $t('home.start_journey') }}</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-gray-300">
          {{ $t('home.access_courses') }}
        </p>
        <router-link to="/courses" class="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg transform hover:-translate-y-1 transition-all duration-200 sm:w-auto">
          {{ $t('home.view_courses') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// No script logic needed for this static landing page for now
</script>
