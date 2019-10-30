#!/usr/bin/env bash

log_path=$1
date_info=`date '+%Y-%m-%d'`
echo "=>parse ${date_info} log"
if [[ ! -d ./log  ]];then
  mkdir ./log
fi

scp ubuntu@192.168.197.43:${log_path}/${date_info}.log ./log

grep "Generated block" ./log/${date_info}.log |grep -v "grep" |awk '{print $1, $2, substr($11,2,64), $13, substr($16,2,64), $19, $23}' >./log/gen-blocks.log
grep "Setting chain lib" ./log/${date_info}.log |grep -v "grep" |awk '{print $1, $2, $11, substr($15,2,64)}' >./log/lib-blocks.log
grep "ShareInValueOfCurrentRound" ./log/${date_info}.log |grep -v "grep" |awk '{print $2, substr($9,1,64), $13}' >./log/consensus-extra-data.log
grep "WARN" ./log/${date_info}.log |grep -v "grep" >./log/warn.log
grep "ERROR" ./log/${date_info}.log |grep -v "grep" >./log/error.log

echo "log handle completed"
echo ""