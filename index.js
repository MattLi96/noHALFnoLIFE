const express = require('express')
const app = express()
const router = express.Router();
const path = require('path');
const generateData = require('./routes/generateData');

let basePath = __dirname;
console.log(basePath)

router.get("/",function(req,res){
  res.sendFile(basePath + "/index.html");
});

app.use(express.static(__dirname + '/public'));

app.use('/data', generateData)
app.use("/",router);

app.use('/src', express.static(__dirname + '/src'));
app.use('/dataRaw', express.static(__dirname + '/dataRaw'));
app.use('/output', express.static(__dirname + '/output'));

let portnum = 8000

app.listen(portnum, function () {
  console.log('Example app listening on port' + portnum + ' !')
})