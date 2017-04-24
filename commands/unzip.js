// https://github.com/cthackers/adm-zip

const splitFile = require('split-file');
const fs = require('fs');
const unzip = require('unzip');

fs.readdir('./dataRaw/zipped', (err, files) => {
    files = files.map((n) => "./dataRaw/zipped/" + n);

    splitFile.mergeFiles(files, './dataRaw/zipped.zip')
        .then(() => {
            console.log('Done with concat!');
            fs.createReadStream('./dataRaw/zipped.zip').pipe(unzip.Extract({ path: './dataRaw' }));
            console.log("Finished");
        })
        .catch((err) => {
            console.log('Error: ', err);
        });
});

