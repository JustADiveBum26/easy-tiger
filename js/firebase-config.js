// Settings for the real guest book and photo wall.
//
// None of these values are secret. They only say WHERE the data lives. What protects the
// data is the rules in firestore.rules. Leave a value empty and the site stays in demo mode.
//
// The house password and the admin email are NOT here. They live in two documents inside
// Firebase (config/house and config/admin) that only Bradley can edit, from the Firebase console.
window.EASY_TIGER_CONFIG = {
  firebase: {
    apiKey: '',
    authDomain: '',
    projectId: '',
    appId: ''
  },
  cloudinary: {
    cloudName: '',
    uploadPreset: ''   // an UNSIGNED preset, set up in the Cloudinary dashboard
  }
};
