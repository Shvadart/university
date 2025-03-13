#!/bin/bash
if [ ! $# -eq 1 ]
then
    echo "Error: check the input data."
    exit 1
fi

until [ "`pwd`" = "/" ]
do
   CURRENT=`pwd`
      echo -e "\n   $(basename "$CURRENT")"
        ls *.$1
        cd ..
done

cd ..
echo -e "\n   /"

ls *.$1
