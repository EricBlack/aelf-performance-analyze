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
    for file in ./*.log.gz
    do
        echo "uncompress file: ${file}"
        gzip ${file} -d
    done
fi

echo "=>parse log: ${log_path}"
data_path=${program_path}/log
if [[ ! -d "${data_path}"  ]];then
    mkdir
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
    grep "Setting chain lib" ${log_path}/${file} |grep -v "grep" |awk '{print $1, $2, $11, substr($15,2,64)}' >>${data_path}/lib-blocks.log
    grep "ShareInValueOfCurrentRound" ${log_path}/${file} |grep -v "grep" |awk '{print $2, substr($9,1,64), $13}' >>${data_path}/consensus-extra-data.log
    grep "WARN" ${log_path}/${file} |grep -v "grep" >>${data_path}/warn.log
    grep "ERROR" ${log_path}/${file} |grep -v "grep" >>${data_path}/error.log
done
echo "log handle completed"
echo ""