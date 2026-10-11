<template>
  <div class="container my-4" style="max-width: 860px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Melbourne Active Transport Map</h3>
      <p class="text-muted mb-0 small">Interactive Route Planning & Carbon Savings Calculator</p>
    </div>

    <div class="row g-3">
      <!-- Left Panel: Route Planner & Hub Search -->
      <div class="col-md-5">
        <!-- Route Planner Card -->
        <div class="card p-3 border bg-white shadow-sm mb-3">
          <h6 class="fw-bold text-dark mb-2">Route Planner</h6>
          <p class="text-muted small mb-2">Select start and end hubs to calculate distance and CO₂ savings.</p>

          <div class="mb-2">
            <label class="form-label small mb-1">Start Location:</label>
            <select v-model="selectedStartId" class="form-select form-select-sm" @change="calculateRoute">
              <option v-for="h in hubs" :key="'start-' + h.id" :value="h.id">{{ h.name }}</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label small mb-1">Destination:</label>
            <select v-model="selectedEndId" class="form-select form-select-sm" @change="calculateRoute">
              <option v-for="h in hubs" :key="'end-' + h.id" :value="h.id">{{ h.name }}</option>
            </select>
          </div>

          <button class="btn btn-dark btn-sm w-100 mb-3" @click="calculateRoute">Plot Route</button>

          <!-- Route Calculation Results -->
          <div v-if="routeResult" class="p-2 bg-light border rounded small">
            <div class="d-flex justify-content-between mb-1">
              <span class="text-muted">Distance:</span>
              <strong>{{ routeResult.distance.toFixed(2) }} km</strong>
            </div>
            <div class="d-flex justify-content-between mb-1">
              <span class="text-muted">Cycling Time:</span>
              <strong class="text-dark">~{{ routeResult.bikeMins }} mins</strong>
            </div>
            <div class="d-flex justify-content-between">
              <span class="text-muted">CO₂ Avoided:</span>
              <strong class="text-success">{{ routeResult.co2Avoided.toFixed(2) }} kg</strong>
            </div>
          </div>
        </div>

        <!-- Hubs List Card -->
        <div class="card p-3 border bg-white shadow-sm">
          <h6 class="fw-bold text-dark mb-2">Active Travel Hubs</h6>
          <div class="input-group input-group-sm mb-2">
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="Filter hub by name..." 
            />
          </div>
          <div class="list-group list-group-flush border-top overflow-auto" style="max-height: 200px;">
            <button 
              v-for="hub in filteredHubs" 
              :key="hub.id"
              class="list-group-item list-group-item-action py-2 px-1 d-flex justify-content-between align-items-center"
              @click="focusHub(hub)"
            >
              <div>
                <strong class="small d-block text-dark">{{ hub.name }}</strong>
                <span class="text-muted small">{{ hub.type }}</span>
              </div>
              <span class="badge bg-light text-dark border">View</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Right Panel: Map Container -->
      <div class="col-md-7">
        <div class="card p-2 border bg-white shadow-sm">
          <div class="d-flex justify-content-between align-items-center mb-2 px-1">
            <small class="text-muted">Melbourne Central Transport Map</small>
            <div class="d-flex align-items-center gap-2">
              <small v-if="locateMessage" class="text-muted">{{ locateMessage }}</small>
              <button class="btn btn-outline-primary btn-sm py-0 px-2" @click="locateUser" :disabled="locating">
                {{ locating ? 'Locating...' : 'Use my location' }}
              </button>
              <button class="btn btn-outline-secondary btn-sm py-0 px-2" @click="resetMapView">
                Reset Center
              </button>
            </div>
          </div>
          <div id="mapContainer" style="height: 460px; width: 100%; border: 1px solid #dee2e6; border-radius: 4px;"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import L from 'leaflet'
import axios from 'axios'

const hubs = [
  { id: 1, name: 'Melbourne Central Bike Hub', type: 'Lockers & Racks', lat: -37.8102, lng: 144.9628 },
  { id: 2, name: 'Flinders St Station Transit Hub', type: 'Station Storage', lat: -37.8180, lng: 144.9671 },
  { id: 3, name: 'Southbank Promenade Refill Point', type: 'Water Refill', lat: -37.8210, lng: 144.9630 },
  { id: 4, name: 'Carlton Gardens Repair Stand', type: 'Public Repair Stand', lat: -37.8055, lng: 144.9715 },
  { id: 5, name: 'Docklands Trailhead Lockers', type: 'Bike Lockers', lat: -37.8160, lng: 144.9450 },
  { id: 6, name: 'Yarra Trail Hub (Richmond)', type: 'Water & Pump', lat: -37.8245, lng: 144.9920 }
]

const searchQuery = ref('')
const selectedStartId = ref(1)
const selectedEndId = ref(2)
const routeResult = ref(null)
const locating = ref(false)
const locateMessage = ref('')
let userMarker = null

let mapInstance = null
let routePolyline = null
let markersGroup = null

const filteredHubs = computed(() => {
  if (!searchQuery.value) return hubs
  const q = searchQuery.value.toLowerCase()
  return hubs.filter(h => h.name.toLowerCase().includes(q) || h.type.toLowerCase().includes(q))
})

onMounted(async () => {
  await nextTick()
  initMap()
  calculateRoute()
})

const initMap = () => {
  const container = document.getElementById('mapContainer')
  if (!container) return

  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }

  mapInstance = L.map('mapContainer').setView([-37.8136, 144.9631], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap'
  }).addTo(mapInstance)

  markersGroup = L.layerGroup().addTo(mapInstance)
  renderMarkers()
}

const renderMarkers = () => {
  if (!markersGroup) return
  markersGroup.clearLayers()

  hubs.forEach(h => {
    const marker = L.marker([h.lat, h.lng])
      .bindPopup(`<b>${h.name}</b><br><small class="text-muted">${h.type}</small>`)
    markersGroup.addLayer(marker)
  })
}

const calculateRoute = async () => {
  const start = hubs.find(h => h.id === Number(selectedStartId.value))
  const end = hubs.find(h => h.id === Number(selectedEndId.value))

  if (!start || !end || start.id === end.id) {
    routeResult.value = null
    if (routePolyline && mapInstance) mapInstance.removeLayer(routePolyline)
    return
  }

  try {
    const url = `https://router.project-osrm.org/route/v1/cycling/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`
    const res = await axios.get(url, { timeout: 4000 })
    if (res.data && res.data.routes && res.data.routes.length > 0) {
      const r = res.data.routes[0]
      const distKm = r.distance / 1000
      const bikeMins = Math.round(r.duration / 60) || 3

      routeResult.value = {
        distance: distKm,
        bikeMins: bikeMins,
        co2Avoided: distKm * 0.192
      }

      const coords = r.geometry.coordinates.map(c => [c[1], c[0]])
      if (routePolyline && mapInstance) mapInstance.removeLayer(routePolyline)
      if (mapInstance) {
        routePolyline = L.polyline(coords, { color: '#212529', weight: 4 }).addTo(mapInstance)
        mapInstance.fitBounds(routePolyline.getBounds(), { padding: [40, 40] })
      }
      return
    }
  } catch (e) {
    console.warn('Real-road routing fallback to straight line:', e.message)
  }

  // Fallback direct distance
  const straight = Math.sqrt(Math.pow(end.lat - start.lat, 2) + Math.pow(end.lng - start.lng, 2)) * 111.32 * 1.3
  routeResult.value = {
    distance: straight,
    bikeMins: Math.round((straight / 16) * 60) || 3,
    co2Avoided: straight * 0.192
  }

  if (routePolyline && mapInstance) mapInstance.removeLayer(routePolyline)
  if (mapInstance) {
    routePolyline = L.polyline([[start.lat, start.lng], [end.lat, end.lng]], {
      color: '#212529',
      weight: 4,
      dashArray: '6, 6'
    }).addTo(mapInstance)
    mapInstance.fitBounds(routePolyline.getBounds(), { padding: [40, 40] })
  }
}

const focusHub = (hub) => {
  if (mapInstance) {
    mapInstance.setView([hub.lat, hub.lng], 16)
    L.popup()
      .setLatLng([hub.lat, hub.lng])
      .setContent(`<b>${hub.name}</b><br><small>${hub.type}</small>`)
      .openOn(mapInstance)
  }
}

const resetMapView = () => {
  if (mapInstance) {
    mapInstance.setView([-37.8136, 144.9631], 13)
  }
}

// Uses the browser's geolocation (with user permission) to centre the map on the user.
const locateUser = () => {
  if (!mapInstance) return
  if (!navigator.geolocation) {
    locateMessage.value = 'Location is not supported by this browser.'
    return
  }

  locating.value = true
  locateMessage.value = ''
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude, accuracy } = pos.coords
      locating.value = false
      if (userMarker) mapInstance.removeLayer(userMarker)
      userMarker = L.circleMarker([latitude, longitude], {
        radius: 8,
        color: '#0d6efd',
        fillColor: '#0d6efd',
        fillOpacity: 0.7
      })
        .bindPopup(`<b>You are here</b><br><small class="text-muted">Accuracy about ${Math.round(accuracy)} m</small>`)
        .addTo(mapInstance)
      mapInstance.setView([latitude, longitude], 15)
      userMarker.openPopup()
      locateMessage.value = 'Location found.'
    },
    (err) => {
      locating.value = false
      locateMessage.value = err.code === 1
        ? 'Location permission was denied.'
        : 'Could not get your location.'
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  )
}
</script>
