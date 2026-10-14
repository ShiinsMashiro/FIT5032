# Ride & Stride Melbourne - Active Transport & Carbon Tracking Platform

A cloud-connected web application built for Monash University **FIT5032 (Internet Applications Development) Assignment 3**.

- **Student Name**: Tujianlong Huang
- **Student ID**: 35272694
- **Live Deployment**: [https://fit5032-bb088.web.app](https://fit5032-bb088.web.app)
- **Cloud Function API**: [https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats](https://us-central1-fit5032-bb088.cloudfunctions.net/calculateEcoStats)

---

## 1. Project Overview

Ride & Stride Melbourne promotes sustainable urban mobility by allowing commuters to log active travel (walking, cycling, public transport, e-scooter), track real-time CO₂ savings, plan street-level routes across Melbourne transport hubs, and generate verifiable commuter achievement certificates.

### Key Features
- **Dashboard & Activity Logger**: Interactive commute logging with instant form validation, weekly goal progress tracking, and reactive summary cards.
- **Dual Interactive Tables**: Two independent data tables for Commuter Trips and Route Reviews, featuring multi-column sorting, keyword search, mode/rating filtering, and 10-row pagination.
- **Interactive Route Map**: Leaflet.js map with OpenStreetMap tiles displaying Melbourne bike hubs, route polyline calculation, and browser geolocation support.
- **Serverless Cloud Aggregation**: 2nd Gen Firebase Cloud Function (`calculateEcoStats`) performing on-demand serverless carbon metrics calculations.
- **Certificate Export & Notifications**: Client-side vector PDF certificate generation and download via jsPDF, with commuter notification dispatch through EmailJS.
- **Authentication & Security**: Firebase Authentication with role-aware interface states (Admin / Commuter) and Cloud Firestore security rules.

---

## 2. Project Structure

```text
A3/
├── public/              # Static assets and icons
├── src/
│   ├── components/      # Reusable UI components (Navbar, etc.)
│   ├── views/           # Routed page views (Home, Trips, Reviews, Map, Email, CloudStats, Login)
│   ├── firebase/        # Firebase client initialization
│   ├── router/          # Vue Router route configuration
│   ├── App.vue          # Root component shell
│   └── main.js          # Application entrypoint
├── index.html           # HTML5 entrypoint
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite build configuration
functions/
├── index.js             # 2nd-gen Cloud Functions backend (calculateEcoStats)
├── package.json         # Cloud Functions dependencies
└── functions.yaml       # Functions deployment metadata
firestore.rules          # Cloud Firestore security rules
firebase.json            # Firebase Hosting and Functions configuration
.firebaserc              # Firebase project alias
```

---

## 3. Demo Credentials

Quick-fill buttons are provided on the login card for convenient evaluation:

| Role | Email | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@fit5032.com` | `admin123` | Administrative controls and bulk database management |
| **Commuter** | `commuter@fit5032.com` | `123456` | Standard trip logging, review submission, and certificate generation |

---

## 4. Local Development & Build

### Prerequisites
- Node.js (v18+ recommended)
- npm

### Running the Frontend
```bash
cd A3
npm install
npm run dev
```
Open [http://localhost:5174/](http://localhost:5174/) in your browser.

### Building for Production
```bash
cd A3
npm run build
```
Production assets are generated in `A3/dist/`.

---

## 5. Technology Stack
- **Frontend**: Vue 3 (Composition API / `<script setup>`), Vite, Vue Router 4, Bootstrap 5
- **Backend / Cloud**: Firebase Authentication, Cloud Firestore, Firebase Cloud Functions (2nd Gen), Firebase Hosting
- **Mapping & Utilities**: Leaflet.js, OpenStreetMap, jsPDF, EmailJS, Axios
