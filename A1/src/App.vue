<template>
  <div class="container my-5" style="max-width: 720px;">
    <!-- Simple Title -->
    <div class="p-3 mb-4 bg-light border text-center">
      <h3 class="text-dark mb-1">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Active Transport & Carbon Tracking</p>
    </div>

    <!-- Summary Metrics -->
    <div class="row g-2 mb-3 text-center">
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">Total Trips</small>
          <strong class="fs-5">{{ totalTrips }}</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">Total Distance</small>
          <strong class="fs-5">{{ totalDistance }} km</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">CO₂ Saved</small>
          <strong class="fs-5 text-success">{{ co2Saved }} kg</strong>
        </div>
      </div>
    </div>

    <!-- Weekly Target Progress Bar -->
    <div class="card p-3 mb-4 border bg-white">
      <div class="d-flex justify-content-between align-items-center mb-1">
        <small class="fw-bold text-secondary">Weekly Community Target (50 km)</small>
        <small class="text-muted">{{ goalProgress }}% Completed</small>
      </div>
      <div class="progress" style="height: 12px;">
        <div
          class="progress-bar bg-success"
          role="progressbar"
          :style="{ width: goalProgress + '%' }"
        ></div>
      </div>
    </div>

    <!-- Part 1: Input Form -->
    <div class="card p-3 mb-4 border bg-white">
      <h5 class="mb-3">1. Add Commuter Trip</h5>

      <form @submit.prevent="addTrip">
        <div class="row mb-3">
          <!-- Commuter Name -->
          <div class="col-md-6 mb-2 mb-md-0">
            <label class="form-label small">Commuter Name:</label>
            <input
              v-model="formData.name"
              type="text"
              class="form-control"
              placeholder="Enter commuter name"
            />
            <div v-if="errors.name" class="text-danger small mt-1">
              {{ errors.name }}
            </div>
          </div>

          <!-- Trip Date -->
          <div class="col-md-6">
            <label class="form-label small">Trip Date:</label>
            <input
              v-model="formData.date"
              type="date"
              class="form-control"
            />
            <div v-if="errors.date" class="text-danger small mt-1">
              {{ errors.date }}
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <!-- Distance -->
          <div class="col-md-6 mb-2 mb-md-0">
            <label class="form-label small">Distance (km):</label>
            <input
              v-model="formData.distance"
              type="number"
              step="any"
              class="form-control"
              placeholder="Enter distance"
            />
            <div v-if="errors.distance" class="text-danger small mt-1">
              {{ errors.distance }}
            </div>
          </div>

          <!-- Transport Mode -->
          <div class="col-md-6">
            <label class="form-label small">Transport Mode:</label>
            <select v-model="formData.mode" class="form-select">
              <option value="">Select mode</option>
              <option value="Walking">Walking</option>
              <option value="Cycling">Cycling</option>
              <option value="Public Transport">Public Transport</option>
            </select>
            <div v-if="errors.mode" class="text-danger small mt-1">
              {{ errors.mode }}
            </div>
          </div>
        </div>

        <!-- Buttons: Submit and Clear -->
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-dark flex-grow-1">
            Submit Trip
          </button>
          <button type="button" class="btn btn-secondary px-4" @click="clearForm">
            Clear
          </button>
        </div>
      </form>
    </div>

    <!-- Part 2: Data Table with Filter -->
    <div class="card p-3 border bg-white">
      <div class="d-flex justify-content-between align-items-center mb-3 gap-2">
        <h5 class="mb-0">2. Trip Records List</h5>
        
        <!-- Simple Filter by Mode -->
        <div class="d-flex align-items-center gap-2">
          <label class="small text-muted mb-0">Filter:</label>
          <select v-model="selectedFilter" class="form-select form-select-sm" style="width: 150px;">
            <option value="All">All Modes</option>
            <option value="Walking">Walking</option>
            <option value="Cycling">Cycling</option>
            <option value="Public Transport">Public Transport</option>
          </select>
        </div>
      </div>

      <div v-if="filteredTrips.length === 0" class="text-center text-muted py-3 border bg-light">
        No trips found for the selected filter.
      </div>

      <table v-else class="table table-bordered mb-0">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th>Date</th>
            <th>Name</th>
            <th>Mode</th>
            <th>Distance</th>
            <th style="width: 14%;" class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredTrips" :key="item.id || index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.name }}</td>
            <td>
              <span class="badge bg-light text-dark border">{{ item.mode }}</span>
            </td>
            <td>{{ item.distance }} km</td>
            <td class="text-center">
              <button
                type="button"
                class="btn btn-sm btn-outline-danger py-0 px-2"
                @click="deleteTrip(item.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Form state object
const formData = ref({
  name: '',
  date: '2026-08-27',
  distance: '',
  mode: ''
})

// Error messages object
const errors = ref({
  name: '',
  date: '',
  distance: '',
  mode: ''
})

// Filter state
const selectedFilter = ref('All')

// Initial sample data (3 simple records)
const tripList = ref([
  { id: 1, date: '2026-08-25', name: 'Liam Cooper', distance: 5.8, mode: 'Cycling' },
  { id: 2, date: '2026-08-26', name: 'Maya Patel', distance: 8.2, mode: 'Public Transport' },
  { id: 3, date: '2026-08-27', name: 'Sarah Jenkins', distance: 3.5, mode: 'Walking' }
])

// Computed statistics
const totalTrips = computed(() => tripList.value.length)

const totalDistance = computed(() => {
  const sum = tripList.value.reduce((acc, curr) => acc + Number(curr.distance || 0), 0)
  return sum.toFixed(1)
})

const co2Saved = computed(() => {
  return (Number(totalDistance.value) * 0.15).toFixed(2)
})

// Community weekly goal (50 km)
const weeklyGoalKm = 50
const goalProgress = computed(() => {
  const percent = (Number(totalDistance.value) / weeklyGoalKm) * 100
  return Math.min(Math.round(percent), 100)
})

// Filtered trips list based on selected transport mode
const filteredTrips = computed(() => {
  if (selectedFilter.value === 'All') {
    return tripList.value
  }
  return tripList.value.filter(item => item.mode === selectedFilter.value)
})

// Validation function
function validateForm() {
  let isValid = true

  if (!formData.value.name.trim()) {
    errors.value.name = 'Please enter a commuter name.'
    isValid = false
  } else {
    errors.value.name = ''
  }

  if (!formData.value.date) {
    errors.value.date = 'Please select a date.'
    isValid = false
  } else {
    errors.value.date = ''
  }

  if (!formData.value.distance || Number(formData.value.distance) <= 0) {
    errors.value.distance = 'Distance must be greater than 0.'
    isValid = false
  } else {
    errors.value.distance = ''
  }

  if (!formData.value.mode) {
    errors.value.mode = 'Please select a transport mode.'
    isValid = false
  } else {
    errors.value.mode = ''
  }

  return isValid
}

// Add a new trip
function addTrip() {
  if (!validateForm()) {
    return
  }

  tripList.value.push({
    id: Date.now(),
    date: formData.value.date,
    name: formData.value.name,
    distance: Number(formData.value.distance),
    mode: formData.value.mode
  })

  clearForm()
}

// Clear form inputs and error messages
function clearForm() {
  formData.value = {
    name: '',
    date: '2026-08-27',
    distance: '',
    mode: ''
  }
  errors.value = {
    name: '',
    date: '',
    distance: '',
    mode: ''
  }
}

// Delete a trip by id
function deleteTrip(id) {
  tripList.value = tripList.value.filter(item => item.id !== id)
}
</script>

<style>
body {
  background-color: #f8fafc;
}
</style>
