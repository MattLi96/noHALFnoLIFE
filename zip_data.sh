#!/usr/bin/env bash

force=false
zip=false
unzip=false
while getopts ":zuf" opt; do
    case ${opt} in
        z) # zip all data
            zip=true
            ;;
        u) # unzip all data
            unzip=true
            ;;
        f) # Currently does nothing
            force=true
            ;;
        \?)
            ;;
    esac
done

pushd dataRaw
pushd zipped
cat x* > zipped.7z
mv -f zipped.7z ..
popd

if ${zip} ; then
    7z u -mx zipped.7z *.xml
    cp -f zipped.7z zipped

    pushd zipped
    rm -f x*
    split -a 3 -b 100m zipped.7z
    rm -f zipped.7z
    git add x*
    popd
fi

if ${unzip} ; then
    7z e zipped.7z
fi
