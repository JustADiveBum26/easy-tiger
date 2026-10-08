// Settings for the real guest book and photo wall.
//
// None of these values are secret. They only say WHERE the data lives. What protects the
// data is the rules in firestore.rules. Leave a value empty and the site stays in demo mode.
//
// The house password and the admin email are NOT here. They live in two documents inside
// Firebase (config/house and config/admin) that only Bradley can edit, from the Firebase console.
window.EASY_TIGER_CONFIG = {
  firebase: {
    apiKey: 'AIzaSyBKSrju1ybKcL26tDMra5I3tmNvEXcqf2w',
    authDomain: 'easy-tiger-como.firebaseapp.com',
    projectId: 'easy-tiger-como',
    appId: '1:817764359074:web:1893e95689aa647d9830fb'
  },
  cloudinary: {
    cloudName: 'czj4oq2l',
    uploadPreset: 'easy-tiger-guests'   // an UNSIGNED preset, set up in the Cloudinary dashboard
  }
};
