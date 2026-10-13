<template>
  <div class="container my-4" style="max-width: 720px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Commuter Certificate & Email Service</h3>
      <p class="text-muted mb-0 small">Official Active Commuter PDF Certificate Generation & Email Dispatch</p>
    </div>

    <div class="card p-4 border bg-white shadow-sm mb-4">
      <form @submit.prevent="handleSendEmail">
        <!-- Recipient -->
        <div class="mb-3">
          <label class="form-label small fw-bold">Recipient Email Address:</label>
          <input 
            v-model="recipient" 
            type="email" 
            class="form-control" 
            placeholder="commuter@monash.edu" 
            required 
          />
        </div>

        <!-- Subject -->
        <div class="mb-3">
          <label class="form-label small fw-bold">Email Subject:</label>
          <input 
            v-model="subject" 
            type="text" 
            class="form-control" 
            required 
          />
        </div>

        <!-- Message Body -->
        <div class="mb-3">
          <label class="form-label small fw-bold">Message Content:</label>
          <textarea 
            v-model="message" 
            rows="3" 
            class="form-control" 
            required
          ></textarea>
        </div>

        <!-- Attachment Box -->
        <div class="p-3 bg-light border rounded mb-3">
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
            <div>
              <strong class="d-block small text-dark">Certificate Document: Ride_and_Stride_Commuter_Certificate.pdf</strong>
              <small class="text-muted">Generated locally with jsPDF. Direct download available; notification dispatched via EmailJS.</small>
            </div>
            <button type="button" class="btn btn-outline-danger btn-sm" @click="downloadPdfCertificate">
              Download PDF Copy
            </button>
          </div>
        </div>

        <!-- Status Alert -->
        <div v-if="statusMessage" class="alert py-2 px-3 small mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'">
          {{ statusMessage }}
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-dark w-100 py-2" :disabled="sending">
          <span v-if="sending" class="spinner-border spinner-border-sm me-1"></span>
          {{ sending ? 'Sending via EmailJS...' : 'Download PDF & Send Email' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { jsPDF } from 'jspdf'
import emailjs from '@emailjs/browser'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase/init'

// ================= EmailJS Configuration =================
const EMAILJS_SERVICE_ID = 'service_3ek3oy4'
const EMAILJS_TEMPLATE_ID = 'template_esjfkah'
const EMAILJS_PUBLIC_KEY = '5kDDUwPUrNKVW3e3p'

const recipient = ref('thua0058@student.monash.edu')
const subject = ref('Ride & Stride Melbourne - Active Commuter Certificate')
const message = ref('Congratulations! Attached is your active transport carbon savings certificate documenting your verified sustainable commutes in Melbourne.')

const sending = ref(false)
const statusMessage = ref('')
const isSuccess = ref(false)

const downloadPdfCertificate = async () => {
  let certTrips = 0
  let certDist = 0
  try {
    const snap = await getDocs(collection(db, 'trips'))
    certTrips = snap.size
    snap.forEach(d => {
      certDist += Number(d.data().distance) || 0
    })
  } catch (e) {
    certTrips = 0
    certDist = 0
  }
  const certCo2 = certDist * 0.192

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
  doc.text(`${recipient.value || 'Commuter'}`, 25, 70)

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
  doc.text(`* Total Logged Trips: ${certTrips} trips`, 35, 112)
  doc.text(`* Cumulative Distance: ${certDist.toFixed(1)} km`, 35, 120)
  doc.text(`* Verified CO2 Emissions Saved: ${certCo2.toFixed(2)} kg`, 35, 128)

  doc.setFontSize(9)
  doc.setTextColor(120, 120, 120)
  doc.text(`Generated on: ${new Date().toLocaleDateString()} | Monash FIT5032 Verification Seal`, 105, 150, { align: 'center' })

  doc.save('Ride_and_Stride_Commuter_Certificate.pdf')
}

const handleSendEmail = async () => {
  if (!recipient.value) {
    alert('Please enter a recipient email address')
    return
  }

  sending.value = true
  statusMessage.value = ''
  isSuccess.value = false

  // 1. Generate PDF and get Base64 data for attachment
  let pdfBase64 = ''
  try {
    let certTrips = 0
    let certDist = 0
    try {
      const snap = await getDocs(collection(db, 'trips'))
      certTrips = snap.size
      snap.forEach(d => {
        certDist += Number(d.data().distance) || 0
      })
    } catch (e) {
      certTrips = 0
      certDist = 0
    }
    const certCo2 = certDist * 0.192

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
    doc.text(`${recipient.value || 'Commuter'}`, 25, 70)

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
    doc.text(`* Total Logged Trips: ${certTrips} trips`, 35, 112)
    doc.text(`* Cumulative Distance: ${certDist.toFixed(1)} km`, 35, 120)
    doc.text(`* Verified CO2 Emissions Saved: ${certCo2.toFixed(2)} kg`, 35, 128)

    doc.setFontSize(9)
    doc.setTextColor(120, 120, 120)
    doc.text(`Generated on: ${new Date().toLocaleDateString()} | Monash FIT5032 Verification Seal`, 105, 150, { align: 'center' })

    // Generate Base64 Data URI for attachment
    pdfBase64 = doc.output('datauristring')
    
    // Also save copy for user
    doc.save('Ride_and_Stride_Commuter_Certificate.pdf')
  } catch (err) {
    statusMessage.value = 'Failed to generate PDF attachment: ' + err.message
    sending.value = false
    return
  }

  // 2. Dispatch email with attachment parameters via EmailJS
  try {
    const params = {
      to_email: recipient.value,
      to_name: recipient.value.split('@')[0],
      user_email: recipient.value,
      subject: subject.value,
      message: message.value,
      attachment_name: 'Ride_and_Stride_Commuter_Certificate.pdf',
      attachment: pdfBase64,
      content: pdfBase64
    }

    await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, params, EMAILJS_PUBLIC_KEY)
    statusMessage.value = `Official Commuter Certificate (PDF) generated as attachment and email sent to ${recipient.value} successfully!`
    isSuccess.value = true
  } catch (err) {
    statusMessage.value = `PDF generated, but EmailJS delivery failed: ${err.text || err.message}`
    isSuccess.value = false
  } finally {
    sending.value = false
  }
}
</script>
