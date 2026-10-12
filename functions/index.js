const { onRequest } = require("firebase-functions/v2/https");
const { setGlobalOptions } = require("firebase-functions/v2");
const { initializeApp, getApps } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");
const cors = require("cors");

// Strictly enforce 1 max instance to prevent any unexpected resource usage
setGlobalOptions({ maxInstances: 1 });

if (getApps().length === 0) {
  initializeApp();
}
const db = getFirestore();

// Browsers may only call these functions from the project's own sites.
// Requests without an Origin header (for example curl) are not affected by CORS.
const corsHandler = cors({
  origin: [
    "https://fit5032-bb088.web.app",
    "https://fit5032-bb088.firebaseapp.com",
    /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/
  ]
});

/**
 * Cloud Function: calculateEcoStats
 * Aggregates the Firestore 'trips' collection to compute total community active distance and CO2 saved.
 */
exports.calculateEcoStats = onRequest((req, res) => {
  corsHandler(req, res, async () => {
    try {
      const tripsSnapshot = await db.collection("trips").get();
      let totalDistance = 0;
      tripsSnapshot.forEach((doc) => {
        const d = doc.data();
        totalDistance += Number(d.distance) || 0;
      });

      const totalTrips = tripsSnapshot.size;
      const totalCo2Saved = totalDistance * 0.192;

      res.status(200).json({
        status: "success",
        totalTrips: totalTrips,
        totalDistance: Number(totalDistance.toFixed(1)),
        totalCo2Saved: Number(totalCo2Saved.toFixed(2)),
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error("Error aggregating eco stats:", error.message);
      res.status(500).json({ error: "Failed to calculate eco stats" });
    }
  });
});
