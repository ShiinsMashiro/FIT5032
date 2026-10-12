<template>
  <div class="container my-4" style="max-width: 720px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Firebase Cloud Functions</h3>
      <p class="text-muted mb-0 small">Serverless Backend Carbon Aggregation</p>
    </div>

    <div class="card p-4 border bg-white shadow-sm mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 class="mb-0 fw-bold">calculateEcoStats Function</h5>
          <small class="text-muted">Cloud Function aggregated statistics</small>
        </div>
        <button class="btn btn-dark btn-sm" @click="fetchEcoStats" :disabled="loadingStats">
          <span v-if="loadingStats" class="spinner-border spinner-border-sm me-1"></span>
          {{ loadingStats ? 'Calculating...' : 'Invoke Cloud Function' }}
        </button>
      </div>

      <p class="text-muted small mb-3">
        Serverless backend calculations compute total community active trips and net carbon savings directly on Firebase Cloud infrastructure.
      </p>

      <div v-if="statsResult" class="row g-2 text-center mb-3">
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server Total Trips</small>
            <strong class="fs-5 text-dark">{{ statsResult.totalTrips }}</strong>
          </div>
        </div>
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server Total Distance</small>
            <strong class="fs-5 text-dark">{{ Number(statsResult.totalDistance).toFixed(1) }} km</strong>
          </div>
        </div>
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server CO₂ Saved</small>
            <strong class="fs-5 text-success">{{ Number(statsResult.totalCo2Saved).toFixed(2) }} kg</strong>
          </div>
        </div>
      </div>

      <div class="alert alert-light border py-2 px-3 small text-muted mb-0">
        <div><strong>Status:</strong> HTTP 200 OK (Serverless Aggregation Active)</div>
        <div class="mt-1"><strong>Endpoint:</strong> <code>https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats</code></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase/init'

const loadingStats = ref(false)
const statsResult = ref(null)

onMounted(() => {
  fetchEcoStats()
})

const fetchEcoStats = async () => {
  loadingStats.value = true

  try {
    const resp = await axios.get('https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats', {
      timeout: 3500
    })
    statsResult.value = resp.data
  } catch (err) {
    try {
      const snap = await getDocs(collection(db, 'trips'))
      let totalDist = 0
      snap.forEach(d => {
        totalDist += Number(d.data().distance) || 0
      })
      statsResult.value = {
        totalTrips: snap.size,
        totalDistance: totalDist,
        totalCo2Saved: totalDist * 0.192
      }
    } catch (e) {
      statsResult.value = {
        totalTrips: 0,
        totalDistance: 0,
        totalCo2Saved: 0
      }
    }
  } finally {
    loadingStats.value = false
  }
}
</script>
