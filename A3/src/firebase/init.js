import { initializeApp, getApps, getApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: 'AIzaSyCDiEFwXO0ShatsplhF0eJAJ4DYj-d6lGA',
  authDomain: 'fit5032-bb088.firebaseapp.com',
  projectId: 'fit5032-bb088',
  storageBucket: 'fit5032-bb088.firebasestorage.app',
  messagingSenderId: '706395938606',
  appId: '1:706395938606:web:bae93d4b30e42c89f124bf'
}

// Initialize Firebase once
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp()
const db = getFirestore(app)
const auth = getAuth(app)

export { app, db, auth }
export default db
