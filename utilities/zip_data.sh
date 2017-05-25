#!/usr/bin/env bash

zip=false
unzip=false
ignore=false
while getopts ":zui" opt; do
    case ${opt} in
        z) # zip all data
            zip=true
            ;;
        u) # unzip all data
            unzip=true
            ;;
        i) # Ignore the current contents of the zipped folder. Use if data is corrupted
            ignore=true
            ;;
        \?)
            ;;
    esac
done

pushd dataRaw
rm -f zipped.7z
if ! ${ignore} ; then
    pushd zipped
    cat x* > zipped.7z
    mv -f zipped.7z ..
    popd
fi

if ${zip} ; then
    7z u -mx=9 zipped.7z *.xml
    mv -f zipped.7z zipped

    pushd zipped
    rm -f x*
    split -a 3 -b 90m zipped.7z
    mv -f zipped.7z ..
    git add x*
    popd
fi

if ${unzip} ; then
    7z e zipped.7z
fi
