#! /usr/bin/python3

import os
import sys

from analyzer import Analyzer
from block import BlockAnalyzer
from configer import config_instance

# log file path
block_log = './log/gen-blocks.log'
lib_log = './log/lib-blocks.log'
warn_log = './log/warn.log'
error_log = './log/error.log'
bad_peer_log = './log/bad-peer.log'
consensus_log = './log/consensus-extra-data.log'
network_hash_log = './log/network-hash.log'
network_peer_log = './log/network-peer.log'
network_req_block_log = './log/network-request-block.log'
network_reply_blocks_log = './log/network-reply-blocks.log'

if __name__ == "__main__":
    config = config_instance.get_config()
    status_info = os.system('bash ./script/parse_date_log.sh {0}'.format(config.LogPath))
    status = status_info >> 8
    if status == 1:
        sys.exit()
    try:
        analyzer = Analyzer(config.Endpoint)
        # analyze block and transaction log
        analyzer.parse_blocks(block_log, config.Start, config.End)
        analyzer.parse_libs(lib_log, config.Start, config.End)
        analyzer.analyze_blocks()
        analyzer.analyze_continue_blocks()
        analyzer.analyze_node_txs()

        # analyze chain block and transactions online
        if config.Online:
            block_analyzer = BlockAnalyzer(config.Endpoint)
            block_analyzer.analyze_chain_txs(analyzer.begin, analyzer.end)

        # analyze network log info
        analyzer.parse_network_hash(network_hash_log)
        analyzer.parse_network_peer(network_peer_log)
        analyzer.parse_network_request_block(network_req_block_log)
        analyzer.parse_network_reply_blocks(network_reply_blocks_log)

        # analyze log info
        analyzer.parse_consensus_data(consensus_log)
        analyzer.parse_warn(warn_log)
        analyzer.parse_error(error_log)
        analyzer.parse_bad_peer(bad_peer_log)
    except Exception as e:
        print('Exception: ', str(e))
        print()

    print('complete log analyze.')
