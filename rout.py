#! /usr/bin/python3

from enum import Enum


class ApiCollection(Enum):
    GetChainStatus = "/api/blockChain/chainStatus"
    GetBlockHeight = "/api/blockChain/blockHeight"
    CreateRawTransaction = "/api/blockChain/rawTransaction"
    GetTransactionPoolStatus = "/api/blockChain/transactionPoolStatus"
    GetBlockByHeight = "/api/blockChain/blockByHeight?blockHeight={0[0]}&includeTransactions={0[1]}"
    GetBlockByHash = "/api/blockChain/block?blockHash={0[0]}&includeTransactions={0[1]}"
    DeploySmartContract = "/api/blockChain/sendTransaction"
    SendTransaction = "/api/blockChain/sendTransaction"
    SendTransactions = "/api/blockChain/sendTransactions"
    SendRawTransaction = "/api/blockChain/sendRawTransaction"
    GetBlockState = "/api/blockChain/blockState?blockHash={0}"
    ExecuteTransaction = "/api/blockChain/executeTransaction"
    ExecuteRawTransaction = "/api/blockChain/executeRawTransaction"
    GetContractFileDescriptorSet = "/api/blockChain/contractFileDescriptorSet?address={0}"
    GetTransactionResult = "/api/blockChain/transactionResult?transactionId={0}"
    GetTransactionResults = "/api/blockChain/transactionResults?blockHash={0[0]}&offset={0[1]}&limit={0[2]}"
    CurrentRoundInformation = "/api/blockChain/currentRoundInformation"

    @staticmethod
    def sub_url(api):
        return api.value
