#!/usr/bin/env bash

#scp ubuntu@$1:/opt/node-1/Logs/2019-10-26.log ./
log_path='/opt/node-1/Logs'
date_info=`date '+%Y-%m-%d'`
echo "=>parse ${date_info} log"

if [[ ! -d ./log  ]];then
  mkdir ./log
fi

grep "Generated block" ${log_path}/${date_info}.log |grep -v "grep" |awk '{print $1, $2, substr($11,2,64), $13, substr($16,2,64), $19, $23}' >./log/gen-blocks.log
grep "Setting chain lib" ${log_path}/${date_info}.log |grep -v "grep" |awk '{print $1, $2, $11, substr($15,2,64)}' >./log/lib-blocks.log
grep "ShareInValueOfCurrentRound" ${log_path}/${date_info}.log |grep -v "grep" |awk '{print $2, substr($9,1,64), $13}' >./log/consensus-extra-data.log
grep "WARN" ${log_path}/${date_info}.log |grep -v "grep" >./log/warn.log
grep "ERROR" ${log_path}/${date_info}.log |grep -v "grep" >./log/error.log

echo "log handle completed"
echo ""