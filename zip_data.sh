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
cat x* > zipped.zip
mv -f zipped.zip ..
popd

if ${zip} ; then
    zip zipped.zip *.xml
    cp -f zipped.zip zipped

    pushd zipped
    rm -f x*
    split -a 3 -b 90m zipped.zip
    rm -f zipped.zip
    git add x*
    popd
fi

if ${unzip} ; then
    ls
    unzip zipped.zip
fi
