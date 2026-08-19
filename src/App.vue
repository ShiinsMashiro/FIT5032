<template>
  <div class="container my-5" style="max-width: 650px;">
    <!-- Simple Title -->
    <div class="p-3 mb-4 bg-light border text-center">
      <h3 class="text-dark mb-1">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Assessment 1.2 Prototype</p>
    </div>

    <!-- Part 1: Input Form (BR B.1 Validation) -->
    <div class="card p-3 mb-4 border">
      <h5 class="mb-3">1. Add Commuter Trip</h5>

      <!-- Error Message -->
      <div v-if="errorMsg" class="alert alert-danger py-2 small mb-3">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="addTrip">
        <div class="mb-3">
          <label class="form-label small">Commuter Name:</label>
          <input
            v-model="commuterName"
            type="text"
            class="form-control"
            placeholder="Enter name"
          />
        </div>

        <div class="mb-3">
          <label class="form-label small">Distance (km):</label>
          <input
            v-model="tripDistance"
            type="number"
            class="form-control"
            placeholder="Enter distance"
          />
        </div>

        <button type="submit" class="btn btn-dark w-100">
          Submit Trip
        </button>
      </form>
    </div>

    <!-- Part 2: Data Table (BR B.2 Dynamic Data) -->
    <div class="card p-3 border">
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

// Form input variables
const commuterName = ref('')
const tripDistance = ref('')
const errorMsg = ref('')

// List of trips
const tripList = ref([
  { name: 'Liam Cooper', distance: 5.8 },
  { name: 'Maya Patel', distance: 8.2 }
])

// Function to add a new trip
function addTrip() {
  // Check if name is empty
  if (commuterName.value === '') {
    errorMsg.value = 'Please enter a name.'
    return
  }

  // Check if distance is valid and positive
  if (tripDistance.value <= 0) {
    errorMsg.value = 'Distance must be greater than 0.'
    return
  }

  // Clear error message
  errorMsg.value = ''

  // Add the new item into the list
  tripList.value.push({
    name: commuterName.value,
    distance: tripDistance.value
  })

  // Clear form inputs
  commuterName.value = ''
  tripDistance.value = ''
}
</script>

<style>
body {
  background-color: #f8fafc;
}
</style>

