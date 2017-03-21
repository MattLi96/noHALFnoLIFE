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
    else
        gzip -k *.xml
    fi
fi
if ${unzip} ; then
    if ${force} ; then
        gunzip -k -f *.gz
    else
        gunzip -k *.gz
    fi
fi

