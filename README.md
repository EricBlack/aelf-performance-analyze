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
1. Analyze without block height range specified.

```shell
python main.py http://192.168.197.40:8000 0 0
```

2. Analyze with block height range specified

```shell
python main.py http://192.168.197.40:8000 1000 2000
```

## TestResult
```
=>analyze log
start time: 2019-10-28 03:30:52,418
end time: 2019-10-28 03:46:32,937
generated blocks: 2630
generated blocks round: 384

=>analyze block
valid blocks:2456, forked blocks: 174

=>analyze continue blocks
average each round generated blocks: 6.85
standard: 163, more blocks: 85, less blocks: 136

=>analyze transactions
total executedTxs: 7892, canceledTxs: 6
average executed txs: 3.0, canceled txs: 0.0

=>analyze warn log
total warn message line: 4001
type=cannot get block hash, count=0
type=Block validate fails before execution, count=185
type=Switch Longest chain, count=186
type=Mining canceled because best chain already updated, count=55
type=others, count=3575

=>analyze warn log
total error message line: 2174
type=Time slot already passed before execution, count=63
type=Error during discover, count=1
type=Request chain 2113 failed, count=0
type=Sender produced too many continuous blocks, count=122
type=Execution cancelled, count=4
type=others, count=1984

```
