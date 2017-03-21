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
        f) # force the zip/unzip (will delete data)
            force=true
            ;;
        \?)
            ;;
    esac
done

pushd dataRaw
if ${zip} ; then
    if ${force} ; then
        gzip -k -f *.xml
        mv -f *.gz zipped
    else
        gzip -k *.xml
        mv *.gz zipped
    fi
    rm -f *.gz
fi

pushd zipped
if ${unzip} ; then
    if ${force} ; then
        gunzip -k -f *.gz
        mv -f *.xml ..
    else
        gunzip -k *.gz
        mv *.xml ..
    fi
    rm -f *.xml
fi
