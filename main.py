#! /usr/bin/python3

import os
from analyzer import Analyzer
from block import BlockAnalyzer
from configer import config_instance

# log file path
block_log = './log/gen-blocks.log'
lib_log = './log/lib-blocks.log'
warn_log = './log/warn.log'
error_log = './log/error.log'
consensus_log = './log/consensus-extra-data.log'

if __name__ == "__main__":
    config = config_instance.get_config()
    status = os.system('bash ./script/parse_log.sh {0}'.format(config.LogPath))
    # status = os.system('bash ./script/parse_remote_log.sh {0}'.format(config.LogPath))
    try:
        analyzer = Analyzer(config.Endpoint)
        analyzer.parse_blocks(block_log, config.Start, config.End)
        analyzer.parse_libs(lib_log, config.Start, config.End)

        analyzer.analyze_blocks()
        analyzer.analyze_continue_blocks()
        analyzer.analyze_node_txs()

        # analyze chain block and transactions online
        if config.Online:
            block_analyzer = BlockAnalyzer(config.Endpoint)
            block_analyzer.analyze_chain_txs(analyzer.begin, analyzer.end)

    except Exception as e:
        print('Exception: ', str(e))
        print()

    analyzer.parse_consensus_data(consensus_log)
    analyzer.parse_warn(warn_log)
    analyzer.parse_error(error_log)

print('complete log analyze.')
