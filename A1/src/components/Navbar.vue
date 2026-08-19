<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/routes">
        Ride & Stride Melbourne
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="navbarContent" class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/routes" active-class="active">
              Route Planner
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/impact" active-class="active">
              Leaderboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/events" active-class="active">
              Equipment Booking
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/portal" active-class="active">
              User Portal
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.nav-link {
  color: #cbd5e1;
}
.nav-link.active {
  color: #ffffff !important;
  font-weight: 600;
}
</style>


