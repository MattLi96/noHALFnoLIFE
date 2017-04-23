/*eslint-env node */
var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');
var filesystem = require("fs");

/* GET users listing. */
router.get('/', function (req, res, next) {
    var options = {
        scriptPath: './src',
        // Uncomment the line below to set python path for recompile
        pythonPath: '/usr/bin/python3',
        args: [true]
    };

    PythonShell.run('main.py', options, function (err, results) {
        console.log('results: %j', results);

        if (err) {
            console.log(err);
            res.send(false)
        }

        res.send(true)
        console.log('finished');
    });
});

router.get('/filelist', function (req, res, next) {
    res.send(getFiles("public/data"));
});

var getFiles = function (dir) {
    var results = [];

    filesystem.readdirSync(dir).forEach(function (file) {
        file = dir + '/' + file;
        var stat = filesystem.statSync(file);

        if (stat && stat.isDirectory()) {
            results = results.concat(_getAllFilesFromFolder(file))
        } else results.push(file);
    });

    // To deal with the timestamps
    function convertToJson(arr) {
        let res = {}

        arr.forEach(function(name){
            
            let k = name.substring(0, name.lastIndexOf("_"));
            let oldList = res[k]
            if(res[k]){
                oldList.push(name)
                res[k] = oldList
            }
            else{
                let newVal = []
                newVal.push(name)
                res[k] = newVal
            }
        });

        return res
    }

    return convertToJson(results);
};

module.exports = router;
