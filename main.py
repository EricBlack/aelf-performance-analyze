#! /usr/bin/python3

import os
import sys

from analyzer import Analyzer
from block import BlockAnalyzer

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

            analyzer = Analyzer(endpoint)
            analyzer.parse_blocks(log, start, end)
            analyzer.analyze_blocks()
            analyzer.analyze_continue_blocks()
            analyzer.analyze_node_txs()

            # analyze chain block and transactions
            if start == 0:
                start = int(analyzer.begin)
            if end == 0:
                end = int(analyzer.end)
            block_analyzer = BlockAnalyzer(endpoint)
            block_analyzer.analyze_chain_txs(start, end)

            analyzer.parse_warn(warn_log)
            analyzer.parse_error(error_log)

    print('complete log analyze.')
