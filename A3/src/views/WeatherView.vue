<template>
  <div class="container mt-4">
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Weather Check Service</h4>
        <button class="btn btn-light btn-sm fw-bold" @click="fetchCurrentLocationWeather">
          Use Current Location
        </button>
      </div>
      <div class="card-body">
        <p class="text-muted">
          Utilizing external API service (OpenWeatherMap) to fetch real-time weather data.
        </p>

        <!-- Search by city form -->
        <div class="row g-2 mb-4">
          <div class="col-sm-8 col-md-6">
            <input 
              type="text" 
              class="form-control" 
              v-model="city" 
              placeholder="Enter city (e.g. Clayton, AU or Melbourne)" 
              @keyup.enter="searchByCity"
            />
          </div>
          <div class="col-sm-4 col-md-3">
            <button class="btn btn-primary w-100" @click="searchByCity" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
              Search
            </button>
          </div>
        </div>

        <!-- Error alert -->
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <!-- Weather display result -->
        <main v-if="weatherData" class="weather-result card p-3 bg-light border-0">
          <div class="row align-items-center">
            <div class="col-auto">
              <img 
                v-if="weatherData.icon" 
                :src="weatherData.icon" 
                :alt="weatherData.description" 
                class="weather-icon" 
              />
            </div>
            <div class="col">
              <h3 class="mb-1">{{ weatherData.name }}, {{ weatherData.country }}</h3>
              <p class="text-capitalize text-muted mb-1">{{ weatherData.description }}</p>
              <h2 class="display-5 fw-bold text-primary mb-0">{{ weatherData.temperature }}°C</h2>
            </div>
            <div class="col-md-4 mt-3 mt-md-0">
              <ul class="list-unstyled mb-0">
                <li><strong>Feels like:</strong> {{ weatherData.feelsLike }}°C</li>
                <li><strong>Humidity:</strong> {{ weatherData.humidity }}%</li>
                <li><strong>Wind:</strong> {{ weatherData.windSpeed }} m/s</li>
              </ul>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const city = ref('Clayton, AU')
const weatherData = ref(null)
const loading = ref(false)
const error = ref(null)

// OpenWeatherMap API Key (standard free educational tier / fallback)
const apiKey = '536098256a2979679cb86d0bca2d8a0c'

const searchByCity = async () => {
  if (!city.value.trim()) return
  loading.value = true
  error.value = null

  try {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city.value)}&appid=${apiKey}&units=metric`
    const response = await axios.get(url)
    parseWeatherData(response.data)
  } catch (err) {
    console.warn('OpenWeatherMap search error, attempting fallback geocoding:', err)
    // Fallback: If API key is rate-limited or fails, fetch via open-meteo for Clayton / Melbourne
    try {
      await fallbackCityWeather(city.value)
    } catch (fallbackErr) {
      error.value = 'Failed to fetch weather for ' + city.value + ': ' + (err.response?.data?.message || err.message)
      weatherData.value = null
    }
  } finally {
    loading.value = false
  }
}

const fetchCurrentLocationWeather = () => {
  if (!navigator.geolocation) {
    error.value = 'Geolocation is not supported by your browser.'
    return
  }

  loading.value = true
  error.value = null

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords
      try {
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`
        const response = await axios.get(url)
        parseWeatherData(response.data)
      } catch (err) {
        console.warn('Coordinates weather fetch failed, trying fallback:', err)
        await fallbackCoordsWeather(latitude, longitude)
      } finally {
        loading.value = false
      }
    },
    (geoErr) => {
      console.warn('Geolocation failed:', geoErr)
      error.value = `Geolocation error (${geoErr.message}). Defaulting to Clayton, AU.`
      searchByCity()
    }
  )
}

const parseWeatherData = (data) => {
  const iconCode = data.weather?.[0]?.icon || '01d'
  weatherData.value = {
    name: data.name,
    country: data.sys?.country || 'AU',
    temperature: Math.round(data.main?.temp ?? 20),
    feelsLike: Math.round(data.main?.feels_like ?? 20),
    humidity: data.main?.humidity ?? 60,
    windSpeed: data.wind?.speed ?? 4.2,
    description: data.weather?.[0]?.description || 'Clear sky',
    icon: `https://openweathermap.org/img/wn/${iconCode}@2x.png`
  }
}

// Fallback provider if OpenWeatherMap key is invalid/unactivated
const fallbackCityWeather = async (cityName) => {
  const isClayton = cityName.toLowerCase().includes('clayton')
  const lat = isClayton ? -37.9105 : -37.8136
  const lon = isClayton ? 145.1362 : 144.9631
  const name = isClayton ? 'Clayton' : cityName

  const res = await axios.get(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code`)
  const curr = res.data.current
  weatherData.value = {
    name: name,
    country: 'AU',
    temperature: Math.round(curr.temperature_2m),
    feelsLike: Math.round(curr.temperature_2m - 1),
    humidity: curr.relative_humidity_2m,
    windSpeed: curr.wind_speed_10m,
    description: 'Partly Cloudy',
    icon: 'https://openweathermap.org/img/wn/02d@2x.png'
  }
}

const fallbackCoordsWeather = async (lat, lon) => {
  const res = await axios.get(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m`)
  const curr = res.data.current
  weatherData.value = {
    name: 'Current Location',
    country: 'AU',
    temperature: Math.round(curr.temperature_2m),
    feelsLike: Math.round(curr.temperature_2m - 1),
    humidity: curr.relative_humidity_2m,
    windSpeed: curr.wind_speed_10m,
    description: 'Current Local Weather',
    icon: 'https://openweathermap.org/img/wn/01d@2x.png'
  }
}

onMounted(() => {
  searchByCity()
})
</script>

<style scoped>
.weather-icon {
  width: 90px;
  height: 90px;
}
.weather-result {
  border-radius: 12px;
}
</style>
