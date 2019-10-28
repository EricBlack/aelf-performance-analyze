#! /usr/bin/python3

import os
import sys

from analyzer import parse_blocks, analyze_blocks, analyze_txs, analyze_continue_blocks, parse_warn, parse_error

if __name__ == "__main__":
    params = sys.argv
    if len(params) != 4:
        print('wrong parameters, three parameters needed.')
    else:
        endpoint = str(params[1])
        start = int(params[2])
        end = int(params[3])
        if start > end != 0:
            print('start height should be bigger than end height.')
        else:
            status = os.system('bash ./script/parse_log.sh')
            log = './log/gen-blocks.log'
            warn_log = './log/warn.log'
            error_log = './log/error.log'

            parse_blocks(log, start, end)
            analyze_blocks(endpoint)
            analyze_continue_blocks()
            analyze_txs()
            parse_warn(warn_log)
            parse_error(error_log)

    print('complete log analyze.')
