/*eslint-env node */
var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');
var filesystem = require("fs");

/* GET users listing. */
router.get('/', function(req, res, next) {
    PythonShell.run('src/main.py', function (err) {
        if (err) throw err;
        console.log('finished');
    });
    
    res.send("Hello World");
});

router.get('/filelist', function(req, res, next){
    res.send(getFiles("public/data"));
});

var getFiles = function(dir) {
    var results = [];

    filesystem.readdirSync(dir).forEach(function(file) {

        file = dir+'/'+file;
        var stat = filesystem.statSync(file);

        if (stat && stat.isDirectory()) {
            results = results.concat(_getAllFilesFromFolder(file))
        } else results.push(file);

    });

    return results;
};

module.exports = router;