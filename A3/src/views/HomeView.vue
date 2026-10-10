<template>
  <div class="container my-4" style="max-width: 720px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Active Transport & Carbon Tracking Platform</p>
    </div>

    <!-- User Authentication -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div v-if="currentUser">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <span class="small text-muted me-1">Logged in as:</span>
            <strong>{{ currentUser.email }}</strong>
            <span class="badge ms-2" :class="currentRole === 'admin' ? 'bg-danger' : 'bg-primary'">
              {{ currentRole === 'admin' ? 'Admin' : 'Commuter' }}
            </span>
          </div>
          <button class="btn btn-sm btn-outline-danger" @click="handleLogout">Logout</button>
        </div>

        <!-- Role-based Admin / Commuter Banner -->
        <div v-if="currentRole === 'admin'" class="alert alert-danger py-2 px-3 mt-3 mb-0 d-flex justify-content-between align-items-center">
          <div>
            <strong>Admin Privileges:</strong>
            <span class="small ms-1">Full administrator access to manage community database.</span>
          </div>
          <button class="btn btn-sm btn-danger py-0 px-2" @click="clearAllTrips" :disabled="clearingTrips">
            {{ clearingTrips ? 'Clearing...' : 'Clear All Records' }}
          </button>
        </div>
        <div v-else class="alert alert-light border py-1 px-3 mt-3 mb-0 text-muted small">
          Standard Commuter Access: Regular trip logging and community review permissions.
        </div>
      </div>
      <div v-else>
        <div class="d-flex flex-wrap gap-2 align-items-center">
          <input 
            v-model="emailInput" 
            type="email" 
            class="form-control form-control-sm flex-grow-1" 
            placeholder="Email (e.g. admin@fit5032.com)" 
          />
          <input 
            v-model="passwordInput" 
            type="password" 
            class="form-control form-control-sm" 
            style="width: 140px;" 
            placeholder="Password" 
          />
          <select v-model="roleInput" class="form-select form-select-sm" style="width: 120px;">
            <option value="commuter">Commuter</option>
            <option value="admin">Admin</option>
          </select>
          <button class="btn btn-sm btn-dark" @click="handleLogin" :disabled="authLoading">Login</button>
          <button class="btn btn-sm btn-outline-secondary" @click="handleRegister" :disabled="authLoading">Register</button>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-2">
          <div class="d-flex gap-2">
            <button type="button" class="btn btn-link btn-sm p-0 text-decoration-none small text-muted" @click="fillQuickAdmin">
              Demo Admin
            </button>
            <span class="text-muted small">|</span>
            <button type="button" class="btn btn-link btn-sm p-0 text-decoration-none small text-muted" @click="fillQuickCommuter">
              Demo Commuter
            </button>
          </div>
          <div v-if="authError" class="text-danger small">{{ authError }}</div>
        </div>
      </div>
    </div>

    <!-- Summary Metrics -->
    <div class="row g-2 mb-3 text-center">
      <div class="col-4">
        <div class="p-2 border bg-white rounded shadow-sm">
          <small class="text-muted d-block">Total Trips</small>
          <strong class="fs-5 text-dark">{{ totalTrips }}</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white rounded shadow-sm">
          <small class="text-muted d-block">Total Distance</small>
          <strong class="fs-5 text-dark">{{ totalDistance.toFixed(1) }} km</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white rounded shadow-sm">
          <small class="text-muted d-block">CO₂ Saved</small>
          <strong class="fs-5 text-success">{{ co2Saved.toFixed(2) }} kg</strong>
        </div>
      </div>
    </div>

    <!-- Weekly Target Progress Bar -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
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

    <!-- 1. Add Commuter Trip -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <h5 class="mb-3 fw-bold">1. Add Commuter Trip</h5>

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
              min="0.1"
              class="form-control"
              placeholder="Enter distance (greater than 0)"
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
              <option value="E-Scooter">E-Scooter</option>
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

    <!-- 2. Trip Records List (Clean table with mode filter & pagination) -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-3 gap-2">
        <div>
          <h5 class="mb-0 fw-bold">2. Trip Records List</h5>
          <small class="text-muted">Total {{ filteredTrips.length }} records found</small>
        </div>
        <div class="d-flex gap-2">
          <input 
            v-model="searchTripKeyword" 
            type="text" 
            class="form-control form-control-sm" 
            style="width: 160px;" 
            placeholder="Search keyword..." 
          />
          <select v-model="selectedTripMode" class="form-select form-select-sm" style="width: 140px;">
            <option value="">All Modes</option>
            <option value="Walking">Walking</option>
            <option value="Cycling">Cycling</option>
            <option value="Public Transport">Public Transport</option>
            <option value="E-Scooter">E-Scooter</option>
          </select>
        </div>
      </div>

      <div v-if="paginatedTrips.length === 0" class="text-center text-muted py-3 border bg-light rounded">
        No trips found matching the criteria.
      </div>

      <div v-else class="table-responsive">
        <table class="table table-bordered mb-2">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th @click="sortTripsBy('date')" style="cursor: pointer;">
              Date <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortTripsBy('name')" style="cursor: pointer;">
              Name <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortTripsBy('mode')" style="cursor: pointer;">
              Mode <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortTripsBy('distance')" style="cursor: pointer;">
              Distance <span class="small text-muted">&#x21C5;</span>
            </th>
            <th style="width: 14%;" class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in paginatedTrips" :key="item.id || index">
            <td>{{ (tripPage - 1) * pageSize + index + 1 }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.name }}</td>
            <td>
              <span class="badge bg-light text-dark border">{{ item.mode }}</span>
            </td>
            <td>{{ Number(item.distance).toFixed(1) }} km</td>
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

      <!-- 10 Rows Limit Pagination Bar -->
      <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top">
        <small class="text-muted">
          Page {{ tripPage }} of {{ totalTripPages }} (10 rows per page)
        </small>
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-secondary" :disabled="tripPage === 1" @click="tripPage--">Previous</button>
          <button 
            v-for="p in totalTripPages" 
            :key="p" 
            class="btn" 
            :class="tripPage === p ? 'btn-dark' : 'btn-outline-secondary'"
            @click="tripPage = p"
          >
            {{ p }}
          </button>
          <button class="btn btn-outline-secondary" :disabled="tripPage === totalTripPages || totalTripPages === 0" @click="tripPage++">Next</button>
        </div>
      </div>
    </div>

    <!-- 3. Route Reviews and Ratings -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-2">
        <h5 class="mb-0 fw-bold">3. Route Reviews and Ratings</h5>
        <div>
          <span class="text-muted small me-1">Average Rating:</span>
          <span class="badge bg-success fs-6">{{ averageRating }} / 5.0</span>
        </div>
      </div>
      <p class="text-muted small mb-3">Community feedback and star ratings for Melbourne active travel routes.</p>

      <!-- Add Review Form -->
      <form @submit.prevent="addReview" class="p-3 bg-light border rounded mb-3">
        <div class="row g-2">
          <div class="col-md-5">
            <label class="form-label small mb-1">Route Name:</label>
            <input
              v-model="reviewForm.route"
              type="text"
              class="form-control form-control-sm"
              placeholder="e.g. Swanston St Bike Lane"
            />
            <div v-if="reviewErrors.route" class="text-danger small mt-1">{{ reviewErrors.route }}</div>
          </div>
          <div class="col-md-3">
            <label class="form-label small mb-1">Rating (1 to 5):</label>
            <select v-model.number="reviewForm.rating" class="form-select form-select-sm">
              <option :value="5">5 - Excellent</option>
              <option :value="4">4 - Good</option>
              <option :value="3">3 - Average</option>
              <option :value="2">2 - Fair</option>
              <option :value="1">1 - Poor</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label small mb-1">Reviewer Name:</label>
            <input
              v-model="reviewForm.author"
              type="text"
              class="form-control form-control-sm"
              placeholder="Your name"
            />
            <div v-if="reviewErrors.author" class="text-danger small mt-1">{{ reviewErrors.author }}</div>
          </div>
          <div class="col-12 mt-2">
            <label class="form-label small mb-1">Comment / Feedback:</label>
            <input
              v-model="reviewForm.comment"
              type="text"
              class="form-control form-control-sm"
              placeholder="Share your active travel experience on this route"
            />
            <div v-if="reviewErrors.comment" class="text-danger small mt-1">{{ reviewErrors.comment }}</div>
          </div>
          <div class="col-12 text-end mt-2">
            <button type="submit" class="btn btn-sm btn-dark">Submit Review</button>
          </div>
        </div>
      </form>

      <!-- Review Filter Bar -->
      <div class="d-flex justify-content-between align-items-center mb-2 gap-2">
        <input 
          v-model="searchReviewKeyword" 
          type="text" 
          class="form-control form-control-sm" 
          style="max-width: 200px;" 
          placeholder="Filter route or author..." 
        />
        <select v-model="selectedReviewRating" class="form-select form-select-sm" style="width: 140px;">
          <option value="">All Ratings</option>
          <option value="5">5 Stars</option>
          <option value="4">4+ Stars</option>
          <option value="3">3+ Stars</option>
        </select>
      </div>

      <!-- Review Table Body -->
      <div class="table-responsive">
      <table class="table table-bordered mb-2">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th @click="sortRevsBy('route')" style="cursor: pointer;">
              Route <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortRevsBy('rating')" style="cursor: pointer; width: 15%;">
              Rating <span class="small text-muted">&#x21C5;</span>
            </th>
            <th>Comment</th>
            <th style="width: 25%;">Author</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="paginatedReviews.length === 0">
            <td colspan="5" class="text-center text-muted py-3">No reviews found.</td>
          </tr>
          <tr v-for="(item, idx) in paginatedReviews" :key="item.id || idx">
            <td>{{ (revPage - 1) * pageSize + idx + 1 }}</td>
            <td class="fw-bold small">{{ item.route }}</td>
            <td>
              <span class="badge bg-secondary">{{ item.rating }} / 5</span>
            </td>
            <td class="small text-muted">{{ item.comment }}</td>
            <td class="small">{{ item.author || item.reviewer || 'Anonymous' }} ({{ item.date }})</td>
          </tr>
        </tbody>
      </table>
      </div>

      <!-- Review Pagination Bar -->
      <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top">
        <small class="text-muted">
          Page {{ revPage }} of {{ totalRevPages }} (10 rows per page)
        </small>
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-secondary" :disabled="revPage === 1" @click="revPage--">Previous</button>
          <button 
            v-for="p in totalRevPages" 
            :key="p" 
            class="btn" 
            :class="revPage === p ? 'btn-dark' : 'btn-outline-secondary'"
            @click="revPage = p"
          >
            {{ p }}
          </button>
          <button class="btn btn-outline-secondary" :disabled="revPage === totalRevPages || totalRevPages === 0" @click="revPage++">Next</button>
        </div>
      </div>
    </div>

    <!-- 4. Active Transport Map & Route Planner -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <h5 class="mb-2 fw-bold">4. Active Travel Map & Route Planner</h5>
      <p class="text-muted small mb-3">
        Interactive Melbourne active transport hubs, route planning, and carbon offset calculations.
      </p>

      <!-- Route Planner Selector -->
      <div class="row g-2 mb-3 p-2 bg-light border rounded">
        <div class="col-md-5">
          <label class="form-label small mb-1">Start Hub:</label>
          <select v-model="selectedStart" class="form-select form-select-sm" @change="updateRoute">
            <option v-for="h in mapHubs" :key="'s-' + h.id" :value="h.id">{{ h.name }} ({{ h.type }})</option>
          </select>
        </div>
        <div class="col-md-5">
          <label class="form-label small mb-1">Destination Hub:</label>
          <select v-model="selectedEnd" class="form-select form-select-sm" @change="updateRoute">
            <option v-for="h in mapHubs" :key="'e-' + h.id" :value="h.id">{{ h.name }} ({{ h.type }})</option>
          </select>
        </div>
        <div class="col-md-2 d-flex align-items-end">
          <button class="btn btn-sm btn-dark w-100" @click="updateRoute">Plot Route</button>
        </div>
      </div>

      <!-- Route Calculation Results -->
      <div v-if="routeMetrics" class="d-flex justify-content-around text-center p-2 mb-3 border bg-white rounded small">
        <div><strong>Distance:</strong> {{ routeMetrics.dist.toFixed(2) }} km</div>
        <div><strong>Cycling Time:</strong> ~{{ routeMetrics.bikeMins }} mins</div>
        <div><strong>CO₂ Avoided:</strong> <span class="text-success fw-bold">{{ routeMetrics.co2.toFixed(2) }} kg</span></div>
      </div>

      <!-- Leaflet Map Container -->
      <div id="simpleMap" style="height: 380px; width: 100%; border: 1px solid #dee2e6; border-radius: 4px;"></div>
    </div>

    <!-- 5. Send Commuter Certificate via Email -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0 fw-bold">5. Commuter Certificate & Email Service</h5>
        <button class="btn btn-sm btn-outline-danger" @click="downloadPdfCertificate">
          Download PDF Certificate
        </button>
      </div>
      <p class="text-muted small mb-3">
        Generate your official active commuter certificate (PDF) and dispatch it via EmailJS.
      </p>

      <div class="input-group input-group-sm mb-3">
        <span class="input-group-text">Recipient</span>
        <input v-model="emailTo" type="email" class="form-control" placeholder="commuter@monash.edu" />
        <button class="btn btn-dark" @click="sendEmail" :disabled="emailSending">
          {{ emailSending ? 'Sending...' : 'Send with PDF Certificate' }}
        </button>
      </div>
      <div v-if="emailStatus" class="alert py-2 px-3 small mb-0" :class="emailStatus.includes('failed') ? 'alert-warning' : 'alert-success'">
        {{ emailStatus }}
      </div>
    </div>

    <!-- 6. Community Cloud Analytics -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0 fw-bold">6. Community Cloud Analytics</h5>
        <button class="btn btn-sm btn-outline-dark" @click="fetchCloudStats" :disabled="statsLoading">
          <span v-if="statsLoading" class="spinner-border spinner-border-sm me-1"></span>
          Refresh Cloud Stats
        </button>
      </div>
      <p class="text-muted small mb-3">
        Serverless aggregation of community trips and carbon savings via Firebase Cloud Functions.
      </p>
      
      <div class="row g-2 text-center mb-2">
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server Total Trips</small>
            <strong class="fs-5 text-dark">{{ cloudTotalTrips }}</strong>
          </div>
        </div>
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server Total Distance</small>
            <strong class="fs-5 text-dark">{{ (cloudTotalCo2 / 0.192).toFixed(1) }} km</strong>
          </div>
        </div>
        <div class="col-4">
          <div class="p-2 border bg-light rounded">
            <small class="text-muted d-block">Server CO₂ Saved</small>
            <strong class="fs-5 text-success">{{ cloudTotalCo2.toFixed(2) }} kg</strong>
          </div>
        </div>
      </div>
      <div v-if="cloudError" class="text-danger small text-center mb-1">{{ cloudError }}</div>
      <div class="text-muted small text-center mt-2">
        Endpoint: <code>https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats</code>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import L from 'leaflet'
import axios from 'axios'
import { jsPDF } from 'jspdf'
import emailjs from '@emailjs/browser'
import { auth, db } from '../firebase/init'
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged 
} from 'firebase/auth'
import { 
  collection, 
  onSnapshot, 
  addDoc, 
  deleteDoc, 
  doc, 
  setDoc, 
  getDoc,
  getDocs,
  serverTimestamp 
} from 'firebase/firestore'

// ================= Firebase Authentication =================
const currentUser = ref(null)
const currentRole = ref('commuter')
const emailInput = ref('')
const passwordInput = ref('')
const roleInput = ref('commuter')
const authError = ref('')
const authLoading = ref(false)
const clearingTrips = ref(false)

const fillQuickAdmin = () => {
  emailInput.value = 'admin@fit5032.com'
  passwordInput.value = 'admin123'
  roleInput.value = 'admin'
}

const fillQuickCommuter = () => {
  emailInput.value = 'commuter@fit5032.com'
  passwordInput.value = '123456'
  roleInput.value = 'commuter'
}

const handleLogin = async () => {
  authError.value = ''
  if (!emailInput.value || !passwordInput.value) {
    authError.value = 'Please enter email and password'
    return
  }
  authLoading.value = true
  try {
    await signInWithEmailAndPassword(auth, emailInput.value, passwordInput.value)
    emailInput.value = ''
    passwordInput.value = ''
  } catch (err) {
    authError.value = 'Login failed: ' + (err.code === 'auth/invalid-credential' ? 'Invalid credentials' : err.message)
  } finally {
    authLoading.value = false
  }
}

const handleRegister = async () => {
  authError.value = ''
  if (!emailInput.value || !passwordInput.value) {
    authError.value = 'Please enter email and password'
    return
  }
  if (passwordInput.value.length < 6) {
    authError.value = 'Password must be at least 6 characters'
    return
  }
  authLoading.value = true
  try {
    const cred = await createUserWithEmailAndPassword(auth, emailInput.value, passwordInput.value)
    await setDoc(doc(db, 'users', cred.user.uid), {
      email: emailInput.value,
      role: roleInput.value
    })
    emailInput.value = ''
    passwordInput.value = ''
  } catch (err) {
    authError.value = 'Registration error: ' + err.message
  } finally {
    authLoading.value = false
  }
}

const handleLogout = async () => {
  await signOut(auth)
}

const clearAllTrips = async () => {
  if (!confirm('Admin confirmation: Are you sure you want to clear all community records from Firestore?')) {
    return
  }
  clearingTrips.value = true
  try {
    const snap = await getDocs(collection(db, 'trips'))
    const deletePromises = snap.docs.map(d => deleteDoc(d.ref))
    await Promise.all(deletePromises)
    tripList.value = []
  } catch (err) {
    console.error('Error clearing trips:', err)
    tripList.value = []
  } finally {
    clearingTrips.value = false
  }
}

// ================= Form & Trip Data (From A1.3) =================
const formData = ref({
  name: '',
  date: new Date().toISOString().split('T')[0],
  distance: '',
  mode: ''
})
const errors = ref({})

// Trips come only from the Firestore 'trips' collection, so the metrics, the table,
// the certificate and the cloud function all use the same records.
const tripList = ref([])

const pageSize = 10
const tripPage = ref(1)
const tripSortKey = ref('date')
const tripSortAsc = ref(false)
const searchTripKeyword = ref('')
const selectedTripMode = ref('')

// Angle brackets are rejected so that markup cannot be stored in the shared records.
const hasMarkup = (text) => /[<>]/.test(text)

const addTrip = async () => {
  errors.value = {}
  const name = formData.value.name.trim()
  if (!name) errors.value.name = 'Please enter name'
  else if (hasMarkup(name)) errors.value.name = 'Name cannot contain < or > characters'
  if (!formData.value.date) errors.value.date = 'Please enter date'
  if (!formData.value.distance || Number(formData.value.distance) <= 0) {
    errors.value.distance = 'Distance must be a positive number greater than 0'
  }
  if (!formData.value.mode) errors.value.mode = 'Please select mode'

  if (Object.keys(errors.value).length > 0) return

  const item = {
    name,
    date: formData.value.date,
    mode: formData.value.mode,
    distance: Number(formData.value.distance)
  }

  // The onSnapshot listener adds the new record to the list, so no local insert is needed.
  try {
    await addDoc(collection(db, 'trips'), { ...item, createdAt: serverTimestamp() })
  } catch (e) {
    alert('Could not save the trip. Please try again.')
    return
  }

  formData.value = {
    name: '',
    date: new Date().toISOString().split('T')[0],
    distance: '',
    mode: ''
  }
}

const clearForm = () => {
  formData.value = {
    name: '',
    date: new Date().toISOString().split('T')[0],
    distance: '',
    mode: ''
  }
  errors.value = {}
}

const deleteTrip = async (id) => {
  tripList.value = tripList.value.filter(t => t.id !== id)
  try {
    await deleteDoc(doc(db, 'trips', id))
  } catch (e) {}
}

const sortTripsBy = (key) => {
  if (tripSortKey.value === key) {
    tripSortAsc.value = !tripSortAsc.value
  } else {
    tripSortKey.value = key
    tripSortAsc.value = true
  }
}

const filteredTrips = computed(() => {
  let list = [...tripList.value]
  if (searchTripKeyword.value) {
    const kw = searchTripKeyword.value.toLowerCase()
    list = list.filter(t => 
      (t.name || '').toLowerCase().includes(kw) ||
      (t.date || '').toLowerCase().includes(kw)
    )
  }
  if (selectedTripMode.value) {
    list = list.filter(t => t.mode === selectedTripMode.value)
  }

  list.sort((a, b) => {
    let va = a[tripSortKey.value]
    let vb = b[tripSortKey.value]
    if (tripSortKey.value === 'distance') {
      va = Number(va) || 0
      vb = Number(vb) || 0
    }
    if (va < vb) return tripSortAsc.value ? -1 : 1
    if (va > vb) return tripSortAsc.value ? 1 : -1
    return 0
  })

  return list
})

const totalTripPages = computed(() => Math.ceil(filteredTrips.value.length / pageSize) || 1)
const paginatedTrips = computed(() => {
  const start = (tripPage.value - 1) * pageSize
  return filteredTrips.value.slice(start, start + pageSize)
})

// Metrics
const totalTrips = computed(() => tripList.value.length)
const totalDistance = computed(() => tripList.value.reduce((acc, t) => acc + (Number(t.distance) || 0), 0))
const co2Saved = computed(() => totalDistance.value * 0.192)
const goalProgress = computed(() => Math.min(100, Math.round((totalDistance.value / 50) * 100)))

// ================= Review Section (A1.3 Table 2) =================
const reviewForm = ref({
  route: '',
  rating: 5,
  author: '',
  comment: ''
})
const reviewErrors = ref({})
const reviewList = ref([])
const revPage = ref(1)
const revSortKey = ref('rating')
const revSortAsc = ref(false)
const searchReviewKeyword = ref('')
const selectedReviewRating = ref('')

const addReview = async () => {
  reviewErrors.value = {}
  const route = reviewForm.value.route.trim()
  const author = reviewForm.value.author.trim()
  const comment = reviewForm.value.comment.trim()

  if (!route) reviewErrors.value.route = 'Please enter route'
  else if (hasMarkup(route)) reviewErrors.value.route = 'Route cannot contain < or > characters'
  if (!author) reviewErrors.value.author = 'Please enter author'
  else if (hasMarkup(author)) reviewErrors.value.author = 'Name cannot contain < or > characters'
  if (!comment) reviewErrors.value.comment = 'Please enter comment'
  else if (hasMarkup(comment)) reviewErrors.value.comment = 'Comment cannot contain < or > characters'

  if (Object.keys(reviewErrors.value).length > 0) return

  const item = {
    route,
    rating: Number(reviewForm.value.rating),
    author,
    comment,
    date: new Date().toISOString().split('T')[0]
  }

  // The onSnapshot listener adds the new record to the list, so no local insert is needed.
  try {
    await addDoc(collection(db, 'reviews'), { ...item, createdAt: serverTimestamp() })
  } catch (e) {
    alert('Could not save the review. Please try again.')
    return
  }

  reviewForm.value = { route: '', rating: 5, author: '', comment: '' }
}

const sortRevsBy = (key) => {
  if (revSortKey.value === key) revSortAsc.value = !revSortAsc.value
  else {
    revSortKey.value = key
    revSortAsc.value = true
  }
}

const filteredReviews = computed(() => {
  let list = [...reviewList.value]
  if (searchReviewKeyword.value) {
    const kw = searchReviewKeyword.value.toLowerCase()
    list = list.filter(r => 
      (r.route || '').toLowerCase().includes(kw) ||
      (r.author || r.reviewer || '').toLowerCase().includes(kw)
    )
  }
  if (selectedReviewRating.value) {
    const mr = parseInt(selectedReviewRating.value)
    if (!isNaN(mr)) list = list.filter(r => r.rating >= mr)
  }

  list.sort((a, b) => {
    let va = a[revSortKey.value]
    let vb = b[revSortKey.value]
    if (revSortKey.value === 'rating') {
      va = Number(va) || 0
      vb = Number(vb) || 0
    }
    if (va < vb) return revSortAsc.value ? -1 : 1
    if (va > vb) return revSortAsc.value ? 1 : -1
    return 0
  })

  return list
})

const totalRevPages = computed(() => Math.ceil(filteredReviews.value.length / pageSize) || 1)
const paginatedReviews = computed(() => {
  const start = (revPage.value - 1) * pageSize
  return filteredReviews.value.slice(start, start + pageSize)
})

const averageRating = computed(() => {
  if (reviewList.value.length === 0) return '0.0'
  const sum = reviewList.value.reduce((acc, r) => acc + (Number(r.rating) || 0), 0)
  return (sum / reviewList.value.length).toFixed(1)
})

// ================= Map Section =================
let map = null
let polyline = null
const selectedStart = ref('1')
const selectedEnd = ref('2')
const routeMetrics = ref(null)

const mapHubs = [
  { id: '1', name: 'Melbourne Central Bike Hub', type: 'Lockers', lat: -37.8102, lng: 144.9628 },
  { id: '2', name: 'Flinders St Station Transit Hub', type: 'Station', lat: -37.8180, lng: 144.9671 },
  { id: '3', name: 'Southbank Promenade Refill Point', type: 'Water Refill', lat: -37.8210, lng: 144.9630 },
  { id: '4', name: 'Carlton Gardens Repair Stand', type: 'Repair Stand', lat: -37.8055, lng: 144.9715 }
]

const initLeafletMap = () => {
  const el = document.getElementById('simpleMap')
  if (!el) return
  if (map) {
    map.remove()
    map = null
  }

  map = L.map('simpleMap').setView([-37.8136, 144.9631], 14)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap'
  }).addTo(map)

  mapHubs.forEach(h => {
    L.marker([h.lat, h.lng])
      .addTo(map)
      .bindPopup(`<b>${h.name}</b><br><small>${h.type}</small>`)
  })

  updateRoute()
}

const updateRoute = async () => {
  const start = mapHubs.find(h => h.id === selectedStart.value)
  const end = mapHubs.find(h => h.id === selectedEnd.value)
  if (!start || !end || start.id === end.id) {
    if (polyline && map) map.removeLayer(polyline)
    routeMetrics.value = null
    return
  }

  try {
    const url = `https://router.project-osrm.org/route/v1/cycling/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`
    const res = await axios.get(url, { timeout: 4000 })
    if (res.data && res.data.routes && res.data.routes.length > 0) {
      const route = res.data.routes[0]
      const d = route.distance / 1000
      const latLngs = route.geometry.coordinates.map(c => [c[1], c[0]])

      routeMetrics.value = {
        dist: d,
        bikeMins: Math.round(route.duration / 60) || 3,
        co2: d * 0.192
      }

      if (polyline && map) map.removeLayer(polyline)
      if (map) {
        polyline = L.polyline(latLngs, { color: '#212529', weight: 4 }).addTo(map)
        map.fitBounds(polyline.getBounds(), { padding: [30, 30] })
      }
      return
    }
  } catch (err) {
    console.warn('Real-road routing fallback to direct calculation:', err.message)
  }

  // Fallback direct road-adjusted estimation
  const straightDist = Math.sqrt(Math.pow(end.lat - start.lat, 2) + Math.pow(end.lng - start.lng, 2)) * 111.32
  const roadDist = straightDist * 1.3
  routeMetrics.value = {
    dist: roadDist,
    bikeMins: Math.round((roadDist / 16) * 60) || 3,
    co2: roadDist * 0.192
  }

  if (polyline && map) map.removeLayer(polyline)
  if (map) {
    polyline = L.polyline([
      [start.lat, start.lng],
      [(start.lat + end.lat) / 2 + 0.002, (start.lng + end.lng) / 2],
      [end.lat, end.lng]
    ], { color: '#212529', weight: 4, dashArray: '6, 6' }).addTo(map)
    map.fitBounds(polyline.getBounds(), { padding: [30, 30] })
  }
}

// ================= Email & jsPDF Certificate =================
const emailTo = ref('thua0058@student.monash.edu')
const emailSending = ref(false)
const emailStatus = ref('')

const downloadPdfCertificate = () => {
  const doc = new jsPDF()
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.setTextColor(33, 37, 41)
  doc.text('Ride & Stride Melbourne', 105, 30, { align: 'center' })

  doc.setFontSize(14)
  doc.setTextColor(40, 167, 69)
  doc.text('Official Active Commuter & Carbon Savings Certificate', 105, 42, { align: 'center' })

  doc.setLineWidth(0.5)
  doc.setDrawColor(200, 200, 200)
  doc.line(25, 48, 185, 48)

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(11)
  doc.setTextColor(50, 50, 50)
  doc.text('This certifies that the active commuter registered under:', 25, 60)
  
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(12)
  doc.setTextColor(0, 0, 0)
  doc.text(`${emailTo.value || 'Commuter'}`, 25, 70)

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(11)
  doc.setTextColor(50, 50, 50)
  doc.text('has actively logged sustainable commutes across Melbourne metropolitan routes.', 25, 80)

  doc.setFillColor(245, 248, 250)
  doc.roundedRect(25, 90, 160, 45, 3, 3, 'F')

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(11)
  doc.text('Summary Achievement Highlights:', 32, 102)

  doc.setFont('helvetica', 'normal')
  doc.text(`* Total Logged Trips: ${totalTrips.value} trips`, 35, 112)
  doc.text(`* Cumulative Distance: ${totalDistance.value.toFixed(1)} km`, 35, 120)
  doc.text(`* Verified CO2 Emissions Saved: ${co2Saved.value.toFixed(2)} kg`, 35, 128)

  doc.setFontSize(9)
  doc.setTextColor(120, 120, 120)
  doc.text(`Generated on: ${new Date().toLocaleDateString()} | Monash FIT5032 Verification Seal`, 105, 150, { align: 'center' })

  doc.save('Ride_and_Stride_Commuter_Certificate.pdf')
}

// ================= EmailJS Configuration =================
const EMAILJS_SERVICE_ID = 'service_3ek3oy4'
const EMAILJS_TEMPLATE_ID = 'template_esjfkah'
const EMAILJS_PUBLIC_KEY = '5kDDUwPUrNKVW3e3p'

const sendEmail = async () => {
  if (!emailTo.value) {
    alert('Please enter an email address')
    return
  }
  emailSending.value = true
  emailStatus.value = ''

  // 1. Download real PDF Certificate via jsPDF
  try {
    downloadPdfCertificate()
  } catch (err) {
    emailStatus.value = 'Failed to generate PDF: ' + err.message
    emailSending.value = false
    return
  }

  // 2. Dispatch via EmailJS if configured
  if (!EMAILJS_SERVICE_ID || !EMAILJS_TEMPLATE_ID || !EMAILJS_PUBLIC_KEY) {
    emailStatus.value = 'Official Commuter Certificate (PDF) downloaded! (Note: Live email sending requires EmailJS credentials)'
    emailSending.value = false
    return
  }

  try {
    const params = {
      to_email: emailTo.value,
      to_name: emailTo.value.split('@')[0],
      user_email: emailTo.value,
      subject: 'Ride & Stride Melbourne - Active Commuter Certificate',
      message: `Congratulations! Your active transport carbon certificate is ready: ${totalDistance.value.toFixed(1)} km travelled and ${co2Saved.value.toFixed(2)} kg CO2 saved.`
    }
    await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, params, EMAILJS_PUBLIC_KEY)
    emailStatus.value = `Official Commuter Certificate (PDF) downloaded, and email successfully dispatched to ${emailTo.value} via EmailJS!`
  } catch (e) {
    emailStatus.value = `PDF Certificate downloaded, but EmailJS delivery failed: ${e.text || e.message}`
  } finally {
    emailSending.value = false
  }
}

// ================= Cloud Functions =================
const statsLoading = ref(false)
const cloudTotalTrips = ref(0)
const cloudTotalCo2 = ref(0)
const cloudError = ref('')

const fetchCloudStats = async () => {
  statsLoading.value = true
  try {
    const res = await axios.get('https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats', { timeout: 3000 })
    cloudTotalTrips.value = res.data.totalTrips ?? 0
    cloudTotalCo2.value = res.data.totalCo2Saved ?? 0
    cloudError.value = ''
  } catch (err) {
    // Do not show local totals under the "Server" labels; report the failure instead.
    cloudTotalTrips.value = 0
    cloudTotalCo2.value = 0
    cloudError.value = 'Server stats unavailable. The Cloud Function could not be reached.'
  } finally {
    statsLoading.value = false
  }
}

// ================= Lifecycle =================
onMounted(async () => {
  onAuthStateChanged(auth, async (u) => {
    currentUser.value = u
    if (u) {
      try {
        const uDoc = await getDoc(doc(db, 'users', u.uid))
        if (uDoc.exists()) currentRole.value = uDoc.data().role || 'commuter'
        else currentRole.value = u.email.includes('admin') ? 'admin' : 'commuter'
      } catch (e) {
        currentRole.value = 'commuter'
      }
    } else {
      currentRole.value = 'commuter'
    }
  })

  // Real-time Firestore sync for trips and reviews (no hardcoded sample rows)
  onSnapshot(collection(db, 'trips'), (snapshot) => {
    tripList.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  }, (err) => console.error('Trips sync failed:', err))

  onSnapshot(collection(db, 'reviews'), (snapshot) => {
    reviewList.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  }, (err) => console.error('Reviews sync failed:', err))

  await nextTick()
  initLeafletMap()
  fetchCloudStats()
})
</script>

<style>
body {
  background-color: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
</style>
