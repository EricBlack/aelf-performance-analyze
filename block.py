#! /usr/bin/python3

import datetime

import api
import rout


class BlockAnalyzer(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.service = api.ApiService(endpoint)

    def chain_status(self):
        response = self.service.get_request(rout.ApiCollection.GetChainStatus)
        chain_status = response.json()
        irreversible_height = chain_status['LastIrreversibleBlockHeight']

        return irreversible_height

    def get_block_info(self, height):
        response = self.service.get_request(rout.ApiCollection.GetBlockByHeight, height, 'false')
        block_info = response.json()

        return {
            'hash': block_info['BlockHash'],
            'time': block_info['Header']['Time'],
            'height': block_info['Header']['Height'],
            'transactions': block_info['Body']['TransactionsCount']
        }

    def analyze_chain_txs(self, start, end):
        print('=>analyze chain transactions')
        total_txs = 0
        blocks = []
        if end < start:
            raise Exception('wrong start and end block height parameter')
        for height in range(start, end):
            block_info = self.get_block_info(height)
            blocks.append(block_info)
            total_txs += block_info['transactions']

        print('check node from height: {0}~{1}'.format(start, end))
        count = end - start
        start_time_str = (blocks[0]['time'])[:-2]
        end_time_str = (blocks[count - 1]['time'])[:-2]
        print('block time: {0}~{1}'.format(start_time_str, end_time_str))

        start_date = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        end_date = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        time_span = (end_date - start_date).seconds
        print('total {0} blocks executed transactions: {1}'.format(count, total_txs))
        print('average transactions/block: {0}'.format(round(total_txs / count, 2)))
        print('average transactions/second: {0}'.format(round(total_txs / time_span, 2)))
        print('average seconds/block: {0}s'.format(round(time_span / count, 3)))
        print()
