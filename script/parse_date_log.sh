#!/usr/bin/env bash

log_path=$1
program_path=`pwd`

# 查询文件夹是否存在
if [[ ! -d "${log_path}" ]];then
    echo "Error: log directory '${log_path}' not existed"
    exit 1
fi

# 判断文件是否为空
count=`ls ${log_path} |wc -w`
if [[ ${count} -eq 0 ]];then
    echo "Error: log directory '{log_path}' is null"
    exit 1
fi

# 遍历文件夹,解压缩日志
cd ${log_path}
file_count=`ls |grep ".gz" |wc -l`
if [[ ${file_count} > 0 ]];then
    for file in ./*.gz
    do
        echo "uncompress file: ${file}"
        gzip ${file} -d
    done
fi

echo "=>parse log: ${log_path}"
data_path=${program_path}/log
if [[ ! -d "${data_path}"  ]];then
    mkdir ${data_path}
else
    rm -rf ${data_path}/*
fi

# 筛选日志
cd ${log_path}
log_files=`ls -ltr | grep ^- |grep ".log" |awk '{print $9}'` #文件按时间倒序排序
for file in ${log_files}
do
    echo "handle file: ${file}"
    grep "Generated block" ${log_path}/${file} |grep -v "grep" |awk '{print $1, $2, substr($11,2,64), $13, substr($16,2,64), $19, $23}' >>${data_path}/gen-blocks.log
    grep "Merging state" ${log_path}/${file} |grep -v "grep" |awk '{print $1, $2, $23, substr($21,2,64)}' >>${data_path}/lib-blocks.log
    grep "ShareInValueOfCurrentRound" ${log_path}/${file} |grep -v "grep" |awk '{print $2, substr($9,1,64), $13}' >>${data_path}/consensus-extra-data.log
    grep "Received announce" ${log_path}/${file} |awk '{print substr($9,2,64)}' |sort |uniq -c >>${data_path}/network-hash.log
    grep "Received announce" ${log_path}/${file} |awk '{print $13}' |sort |uniq -c |sort -n >>${data_path}/network-peer.log
    grep "Getting block by hash" ${log_path}/${file} |awk '{print $16}' |sort -n |uniq -c |sort -n >>${data_path}/network-request-block.log
    grep "Calculating max blocks count based on\|Current blockchain mining status" -A 4 ${log_path}/${file} >>${data_path}/block-status.log
    grep "Replied to" ${log_path}/${file} |awk '{print $11, $16}' >>${data_path}/network-reply-blocks.log
    grep "WARN" ${log_path}/${file} |grep -v "grep\|WARNING" >>${data_path}/warn.log
    grep "ERROR" ${log_path}/${file} |grep -v "grep" >>${data_path}/error.log
    #bad peer
    count=`grep "bad peer" ${log_path}/${file} |wc -l`
    if [[ ${count} > 0 ]];then
        echo "${file}  ${count}" >>${data_path}/bad-peer.log
    fi
done
echo "log handle completed"
echo ""