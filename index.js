const express = require('express')
const app = express()
const router = express.Router();
const path = require('path');
const generateData = require('./routes/generateData');

let basePath = __dirname;

router.get("/",function(req,res){
  res.sendFile(basePath + "/index.html");
});

app.use(express.static(__dirname + '/public'));

app.use('/data', generateData)
app.use("/",router);

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})