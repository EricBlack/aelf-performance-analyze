#!/usr/bin/env bash

check=`which pip3 |wc -l`
if  [[ check == 0 ]]
then
    echo 'install package: pip3 and PyMySQL'
    apt install python3-pip -y
    pip3 install PyMySQL
fi

check=`pip3 list |grep PyMySQL |wc -l`
if  [[ check == 0 ]]
then
    echo 'install package: PyMySQL'
    pip3 install PyMySQL
fi

echo 'install complete.'

