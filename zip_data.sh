#!/usr/bin/env bash

force=false
zip=false
unzip=false
ignore=false
while getopts ":zufi" opt; do
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
        i) # Ignore the current contents of the zipped folder. Use if data is corrupted
            ignore=true
            ;;
        \?)
            ;;
    esac
done

pushd dataRaw
if ! ${ignore} ; then
    pushd zipped
    cat x* > zipped.zip
    mv -f zipped.zip ..
    popd
fi

if ${zip} ; then
    zip zipped.zip *.xml
    mv -f zipped.zip zipped

    pushd zipped
    rm -f x*
    split -a 3 -b 90m zipped.zip
    mv -f zipped.zip ..
    git add x*
    popd
fi

if ${unzip} ; then
    unzip zipped.zip
fi
