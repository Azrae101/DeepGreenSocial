// COPY THIS FILE TO firebase-config.js AND ADD YOUR ACTUAL FIREBASE CREDENTIALS

const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.firebasestorage.app",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase (compat version for simplicity)
firebase.initializeApp(firebaseConfig);

// Make Firebase services globally available
const auth = firebase.auth();
const db = firebase.firestore();
const storage = firebase.storage();

// Export for modular use if needed
window.firebaseApp = firebase.app();
window.firebaseAuth = auth;
window.firebaseDb = db;
window.firebaseStorage = storage;
