// Default requires for Express
const express = require('express');
const app = express();
const router = express.Router();
const path = require('path');

// File for REST API endpoint /data
const generateData = require('./routes/generateData');

// Base Directory
let basePath = __dirname;

// Default Page
router.get("/",function(req,res){
  res.sendFile(basePath + "/index.html");
});

// Make sure to include all files in /public
app.use('/public', express.static(__dirname + '/public'));

// Map /data to the REST API endpoint
app.use('/data', generateData);
app.use("/",router);

// Make sure that the app can use other folders
app.use('/src', express.static(__dirname + '/src'));
app.use('/dataRaw', express.static(__dirname + '/dataRaw'));
app.use('/output', express.static(__dirname + '/output'));

// Port Number to start on
let portnum = 8000;

// Listen
app.listen(portnum, function () {
  console.log('Example app listening on PORT: ' + portnum + ' !');
})