/*eslint-env node */
var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');

/* GET users listing. */
router.get('/', function(req, res, next) {
    PythonShell.run('src/main.py', function (err) {
        if (err) throw err;
        console.log('finished');
    });
    
    res.send("Hello World");
});

module.exports = router;