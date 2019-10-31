# aelf-performance-analyze

## Scripts used to analyze aelf node performance based on node log.

Analyze one node generated blocks and executed transactions in specified height range.

## Description
Following data would be record:
1. block generate start to end time
2. block generate total numbers and round numbers
3. valid blocks and invalid blocks(forked blocks)
4. executed transactions and canceled transactions
5. average block executed and canceled transactions
6. different type warn and error messages count 

## Usage
Parameter information:
- config-section: refer config-ini, specified log path and endpoint service address
- start: start analyze block height
- end: end analyze block height
- online: whether chain api service works or not, if not would not analyze blocks transaction status.
1. Analyze without block height range specified.

```shell
python main.py [config-section] 0 0 true
```

2. Analyze with block height range specified

```shell
python main.py [config-section] 1000 2000 true
```

## TestResult
```
=>parse 2019-10-31 log
log handle completed

=>parse blocks
start time: 2019-10-31 09:05:34,198
end time: 2019-10-31 10:31:50,252
generated blocks: 518
generated blocks round: 154

=>parse libs
lib height from: 50028~54000
lib time: 2019-10-31 09:07:46,446~2019-10-31 10:33:37,051
average second/block: 1.297s

=>analyze blocks
valid blocks:361, forked blocks: 156, none lib blocks: 1
forked block percent: 30.12%

=>analyze continue blocks
average each round generated blocks: 3.36
standard: 0, more blocks: 1, less blocks: 153

=>analyze node transactions
total executedTxs: 34892, canceledTxs: 70167
average each block executed txs: 67.36, canceled txs: 135.46

=>analyze chain transactions
check node from height: 50028~54000
block time: 2019-10-31T09:05:33.895585~2019-10-31T10:31:48.251944
total 3972 blocks executed transactions: 490746
average transactions/block: 123.55
average transactions/second: 94.85
average seconds/block: 1.303s

=>analyze consensus extra data log
type: 0-10  ms, count: 5
type: 10-50 ms, count: 2
type: 50-100ms, count: 875
type: >100  ms, count: 1966

=>analyze warn log
total warn message line: 39449
type=Switch Longest chain, count=411
type=Block validate fails before execution, count=407
type=Mining canceled because best chain already updated, count=196
type=cannot get block hash, count=1947
type=others, count=36488

=>analyze error log
total error message line: 2469
type=Error during discover, count=19
type=Time slot already passed before execution, count=320
type=Sender produced too many continuous blocks, count=87
type=Execution cancelled, count=0
type=Request chain 2113 failed, count=383
type=others, count=1660

complete log analyze.

```
