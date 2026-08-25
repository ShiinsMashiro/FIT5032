<template>
  <div class="container my-5" style="max-width: 650px;">
    <!-- Simple Title -->
    <div class="p-3 mb-4 bg-light border text-center">
      <h3 class="text-dark mb-1">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Active Transport & Carbon Tracking</p>
    </div>

    <!-- Part 1: Input Form (BR B.1 Validation) -->
    <div class="card p-3 mb-4 border bg-white">
      <h5 class="mb-3">1. Add Commuter Trip</h5>

      <!-- Error Message -->
      <div v-if="errorMsg" class="alert alert-danger py-2 small mb-3">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="addTrip">
        <div class="mb-3">
          <label class="form-label small">Commuter Name:</label>
          <input
            v-model="formData.name"
            type="text"
            class="form-control"
            placeholder="Enter commuter name"
          />
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
          </div>

          <div class="col-md-6">
            <label class="form-label small">Transport Mode:</label>
            <select v-model="formData.mode" class="form-select">
              <option value="">Select mode</option>
              <option value="Walking">Walking</option>
              <option value="Cycling">Cycling</option>
              <option value="Public Transport">Public Transport</option>
            </select>
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
import { ref } from 'vue'

// Form state
const formData = ref({
  name: '',
  distance: '',
  mode: ''
})

const errorMsg = ref('')

// List of trips
const tripList = ref([
  { name: 'Liam Cooper', distance: 5.8 },
  { name: 'Maya Patel', distance: 8.2 }
])

// Function to add a new trip
function addTrip() {
  if (!formData.value.name.trim()) {
    errorMsg.value = 'Please enter a commuter name.'
    return
  }

  if (!formData.value.distance || Number(formData.value.distance) <= 0) {
    errorMsg.value = 'Distance must be greater than 0.'
    return
  }

  if (!formData.value.mode) {
    errorMsg.value = 'Please select a transport mode.'
    return
  }

  errorMsg.value = ''

  tripList.value.push({
    name: formData.value.name,
    distance: Number(formData.value.distance)
  })

  clearForm()
}

// Clear form inputs
function clearForm() {
  formData.value = {
    name: '',
    distance: '',
    mode: ''
  }
  errorMsg.value = ''
}
</script>

<style>
body {
  background-color: #f8fafc;
}
</style>
