#! /usr/bin/python3

import os
import sys

from analyzer import Analyzer
from block import BlockAnalyzer


def str2bool(info):
    if info in ['true', 'TRUE', 'True', 'y', 'Y']:
        return True
    return False


if __name__ == "__main__":
    params = sys.argv
    if len(params) != 5:
        print('wrong parameters, four parameters needed.')
    else:
        endpoint = str(params[1])
        start = int(params[2])
        end = int(params[3])
        online = str2bool(params[4])
        if start > end != 0:
            print('start height should be bigger than end height.')
        else:
            status = os.system('bash ./script/parse_log.sh')
            # status = os.system('bash ./script/parse_remote_log.sh')
            block_log = './log/gen-blocks.log'
            lib_log = './log/lib-blocks.log'
            warn_log = './log/warn.log'
            error_log = './log/error.log'

            try:
                analyzer = Analyzer(endpoint)
                analyzer.parse_blocks(block_log, start, end)
                analyzer.parse_libs(lib_log, start, end)

                analyzer.analyze_blocks()
                analyzer.analyze_continue_blocks()
                analyzer.analyze_node_txs()

                # analyze chain block and transactions online
                if online:
                    block_analyzer = BlockAnalyzer(endpoint)
                    block_analyzer.analyze_chain_txs(analyzer.begin, analyzer.end)

            except Exception as e:
                print('Exception: ', str(e))

            analyzer.parse_warn(warn_log)
            analyzer.parse_error(error_log)

    print('complete log analyze.')
