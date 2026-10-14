<template>
  <div class="container mt-4">
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Leaflet Map & Geolocation</h4>
        <button class="btn btn-light btn-sm fw-bold" @click="locateUser">
          Locate My Current Location
        </button>
      </div>
      <div class="card-body">
        <p class="text-muted mb-3">
          Interactive map created using Leaflet and OpenStreetMap. Click the button above to test
          HTML5 Geolocation (<code>navigator.geolocation</code>), or click anywhere on the map to inspect coordinates.
        </p>

        <!-- Status & Geolocation Message -->
        <div v-if="geoMessage" :class="['alert', geoError ? 'alert-danger' : 'alert-info', 'py-2']" role="alert">
          {{ geoMessage }}
        </div>

        <!-- Leaflet Map Container -->
        <div id="map" class="map-container border rounded"></div>

        <!-- Coordinates Summary Card -->
        <div class="row mt-3 g-2">
          <div class="col-md-6">
            <div class="card bg-light p-2">
              <small class="text-muted">Current Center:</small>
              <strong>Lat: {{ centerLat.toFixed(4) }}, Lng: {{ centerLng.toFixed(4) }}</strong>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card bg-light p-2">
              <small class="text-muted">User Geolocation:</small>
              <strong v-if="userCoords">
                Lat: {{ userCoords.latitude.toFixed(4) }}, Lng: {{ userCoords.longitude.toFixed(4) }} (Accuracy: ±{{ Math.round(userCoords.accuracy) }}m)
              </strong>
              <span v-else class="text-secondary">Not located yet (Click "Locate My Current Location")</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix default Leaflet icon paths in Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
})

let mapInstance = null
let userMarker = null

const centerLat = ref(-37.9105)
const centerLng = ref(145.1362)
const geoMessage = ref('')
const geoError = ref(false)
const userCoords = ref(null)

const campusLocations = [
  {
    name: 'Monash Clayton - Main Campus',
    coords: [-37.9105, 145.1362],
    description: 'Wellington Road, Clayton VIC 3800'
  },
  {
    name: 'Matheson Library (Clayton)',
    coords: [-37.9135, 145.1325],
    description: 'Sir Louis Matheson Library - Monash University'
  },
  {
    name: 'Hargrave-Andrew Library (Clayton)',
    coords: [-37.9098, 145.1332],
    description: 'Engineering, Science and IT Library'
  },
  {
    name: 'Monash Caulfield Campus',
    coords: [-37.8770, 145.0443],
    description: '900 Dandenong Rd, Caulfield East VIC 3145'
  }
]

onMounted(() => {
  initMap()
})

onBeforeUnmount(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})

const initMap = () => {
  // 1. Initialize map centered at Monash Clayton
  mapInstance = L.map('map').setView([centerLat.value, centerLng.value], 14)

  // 2. Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mapInstance)

  // 3. Add default campus & library markers
  campusLocations.forEach((loc) => {
    L.marker(loc.coords)
      .addTo(mapInstance)
      .bindPopup(`<strong>${loc.name}</strong><br>${loc.description}`)
  })

  // 4. Handle map click to show clicked coordinates
  mapInstance.on('click', (e) => {
    L.popup()
      .setLatLng(e.latlng)
      .setContent(`<strong>Clicked Location:</strong><br>Lat: ${e.latlng.lat.toFixed(5)}<br>Lng: ${e.latlng.lng.toFixed(5)}`)
      .openOn(mapInstance)
  })

  // 5. Track center changes
  mapInstance.on('move', () => {
    const center = mapInstance.getCenter()
    centerLat.value = center.lat
    centerLng.value = center.lng
  })
}

const locateUser = () => {
  if (!navigator.geolocation) {
    geoError.value = true
    geoMessage.value = 'Geolocation is not supported by your browser.'
    return
  }

  geoError.value = false
  geoMessage.value = 'Locating your current position...'

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude, accuracy } = position.coords
      userCoords.value = { latitude, longitude, accuracy }
      geoMessage.value = `Location found! Lat: ${latitude.toFixed(4)}, Lng: ${longitude.toFixed(4)}`
      geoError.value = false

      // Remove existing user marker if present
      if (userMarker) {
        mapInstance.removeLayer(userMarker)
      }

      // Add a distinct marker for user position
      userMarker = L.marker([latitude, longitude])
        .addTo(mapInstance)
        .bindPopup(`<strong>You are here!</strong><br>Lat: ${latitude.toFixed(5)}<br>Lng: ${longitude.toFixed(5)}<br>Accuracy: ±${Math.round(accuracy)}m`)
        .openPopup()

      // Fly to user's location
      mapInstance.flyTo([latitude, longitude], 15, {
        duration: 1.5
      })
    },
    (err) => {
      console.warn('Geolocation error:', err)
      geoError.value = true
      geoMessage.value = `Geolocation error: ${err.message}. Using Monash Clayton campus as default.`
      // Fallback: zoom to Monash Clayton
      mapInstance.flyTo([-37.9105, 145.1362], 15)
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
  )
}
</script>

<style scoped>
.map-container {
  height: 520px;
  width: 100%;
  z-index: 1;
}
</style>
