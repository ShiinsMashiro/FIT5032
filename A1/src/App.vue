<template>
  <div class="container my-5" style="max-width: 700px;">
    <!-- Simple Title -->
    <div class="p-3 mb-4 bg-light border text-center">
      <h3 class="text-dark mb-1">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Active Transport & Carbon Tracking</p>
    </div>

    <!-- Summary Metrics -->
    <div class="row g-2 mb-4 text-center">
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

    <!-- Part 1: Input Form (BR B.1 Validation) -->
    <div class="card p-3 mb-4 border bg-white">
      <h5 class="mb-3">1. Add Commuter Trip</h5>

      <form @submit.prevent="addTrip">
        <div class="mb-3">
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

        <div class="row mb-3">
          <div class="col-md-6">
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

    <!-- Part 2: Data Table (BR B.2 Dynamic Data) -->
    <div class="card p-3 border bg-white">
      <h5 class="mb-3">2. Trip Records List</h5>

      <table class="table table-bordered mb-0">
        <thead class="table-light">
          <tr>
            <th>No.</th>
            <th>Name</th>
            <th>Distance</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in tripList" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.distance }} km</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Form state
const formData = ref({
  name: '',
  distance: '',
  mode: ''
})

// Error messages
const errors = ref({
  name: '',
  distance: '',
  mode: ''
})

// List of trips
const tripList = ref([
  { name: 'Liam Cooper', distance: 5.8 },
  { name: 'Maya Patel', distance: 8.2 }
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

// Form validation function
function validateForm() {
  let isValid = true

  if (!formData.value.name.trim()) {
    errors.value.name = 'Please enter a commuter name.'
    isValid = false
  } else {
    errors.value.name = ''
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

// Function to add a new trip
function addTrip() {
  if (!validateForm()) {
    return
  }

  tripList.value.push({
    name: formData.value.name,
    distance: Number(formData.value.distance)
  })

  clearForm()
}

// Clear form inputs and errors
function clearForm() {
  formData.value = {
    name: '',
    distance: '',
    mode: ''
  }
  errors.value = {
    name: '',
    distance: '',
    mode: ''
  }
}
</script>

<style>
body {
  background-color: #f8fafc;
}
</style>
