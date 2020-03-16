importScripts('https://www.gstatic.com/firebasejs/4.4.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.4.0/firebase-messaging.js');
  var firebaseConfig = {
    apiKey: "AIzaSyCl03SFdOUdkNG4bpvHfcfcN9Bm0Hqn_i4",
    authDomain: "testfirebase-e7902.firebaseapp.com",
    databaseURL: "https://testfirebase-e7902.firebaseio.com",
    projectId: "testfirebase-e7902",
    storageBucket: "testfirebase-e7902.appspot.com",
    messagingSenderId: "156298674124",
    appId: "1:156298674124:web:8faa7486f6c5df0ebee769",
    measurementId: "G-NPDLVPVNK3"
  };
firebase.initializeApp(config);
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function(payload) {
 const title = 'Hello World';
 const options = {
  body: payload.data.body
 };
 return self.registration.showNotification(title, options);
});