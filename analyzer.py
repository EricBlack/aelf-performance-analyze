#! /usr/bin/python3

import api
import rout

generate_blocks = {}
valid_blocks = {}
invalid_blocks = {}
continue_blocks = {}


def read_file_line(file_name):
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line


# parse message
# 2019-10-26 00:00:53,639 6bb39eab787b7a34c1ebf7cdc56daeb8eec3d69e49223a2f1b20fced3fc84a1e 282441 7232888909c8776fc0e3d581335ac3cadf38e91b24e1892a83996732dd59bdaf 3, 0


def parse_blocks(log_file, low_height, high_height):
    print("=>analyze log")

    start_height = 0
    end_height = 0

    lines = read_file_line(log_file)
    for line in lines:
        message = line.split(" ")
        time = message[0] + ' ' + message[1]
        current_hash = message[2]
        height = int(message[3])
        if low_height != 0 and height < low_height:
            continue
        if high_height != 0 and height > high_height:
            break

        previous_hash = message[4]
        executed_txs = int(str(message[5]).replace(",", ""))
        canceled_txs = int(message[6])

        block_info = {'time': time, 'height': height, 'hash': current_hash, 'previous': previous_hash,
                      'executed_txs': executed_txs, 'canceled_txs': canceled_txs}
        generate_blocks[str(height)] = block_info

        if start_height == 0:
            start_height = height
            end_height = height
        elif end_height == height - 1:
            end_height += 1
        else:
            number = str(len(continue_blocks) + 1)
            continue_info = {"start": start_height, "end": end_height, "blocks": end_height - start_height + 1}
            continue_blocks[number] = continue_info
            start_height = height
            end_height = height

    begin = sorted(generate_blocks.keys())[0]
    end = sorted(generate_blocks.keys())[len(generate_blocks) - 1]
    print('start time: {0}'.format(generate_blocks[begin]['time']))
    print('end time: {0}'.format(generate_blocks[end]['time']))
    print('generated blocks: {0}'.format(len(generate_blocks)))
    print('generated blocks round: {0}'.format(len(continue_blocks)))
    print()


def analyze_blocks(endpoint):
    print("=>analyze block")
    service = api.ApiService(endpoint)

    for height in generate_blocks.keys():
        block = service.get_request(rout.ApiCollection.GetBlockByHeight, height, "false")
        if block.status_code != 200:
            continue
        block_hash = block.json()['BlockHash']
        if block_hash == generate_blocks[height]["hash"]:
            valid_blocks[height] = generate_blocks[height]
        else:
            invalid_blocks[height] = generate_blocks[height]

    print('valid blocks:{0}, forked blocks: {1}'.format(len(valid_blocks), len(invalid_blocks)))
    print()


def analyze_continue_blocks():
    print("=>analyze continue blocks")
    enough_no = 0
    standard_no = 0
    less_no = 0
    for number in continue_blocks:
        block = continue_blocks[number]
        if block['blocks'] > 8:
            enough_no += 1
            # print('blocks: {0}~{1}, count: {2}'.format(block['start'], block['end'], block['blocks']))
        elif block['blocks'] == 8:
            standard_no += 1
        else:
            less_no += 1
            # print('blocks: {0}~{1}, count: {2}'.format(block['start'], block['end'], block['blocks']))

    print('average each round generated blocks: {0}'.format(round(len(generate_blocks) / len(continue_blocks), 2)))
    print('standard: {0}, more blocks: {1}, less blocks: {2}'.format(standard_no, enough_no, less_no))
    print()


def analyze_txs():
    print("=>analyze transactions")
    executed_amounts = 0
    canceled_amounts = 0
    count = len(generate_blocks)
    for height in generate_blocks:
        block_info = generate_blocks[height]
        executed_amounts += block_info['executed_txs']
        canceled_amounts += block_info['canceled_txs']

    print('total executedTxs: {0}, canceledTxs: {1}'.format(executed_amounts, canceled_amounts))
    print('average executed txs: {0}, canceled txs: {1}'.format(round(executed_amounts / count, 2),
                                                                round(canceled_amounts / count, 2)))
    print()


def parse_warn(warn_log):
    print("=>analyze warn log")
    warn_summary = {}
    for key in warn_msgs.keys():
        warn_summary[key] = 0

    lines = read_file_line(warn_log)
    count = file_line_count(warn_log)
    print("total warn message line: {0}".format(count))

    for line in lines:
        for key in warn_msgs.keys():
            if warn_msgs[key] in line:
                warn_summary[key] += 1
                break

    other_warn = count
    for key in warn_summary:
        other_warn -= warn_summary[key]
        print('type={0}, count={1}'.format(warn_msgs[key], warn_summary[key]))
    print('type=others, count={0}'.format(other_warn))
    print()


def parse_error(error_log):
    print("=>analyze warn log")
    error_summary = {}
    for key in error_msgs.keys():
        error_summary[key] = 0

    lines = read_file_line(error_log)
    count = file_line_count(error_log)
    print("total error message line: {0}".format(count))
    for line in lines:
        for key in error_msgs.keys():
            if error_msgs[key] in line:
                error_summary[key] += 1
                break

    other_error = count
    for key in error_summary:
        other_error -= error_summary[key]
        print('type={0}, count={1}'.format(error_msgs[key], error_summary[key]))
    print('type=others, count={0}'.format(other_error))
    print()


def file_line_count(file):
    count = -1
    for count, line in enumerate(open(file, 'rU')):
        pass
    count += 1

    return count


warn_msgs = {
    "warn1": "Switch Longest chain",
    "warn2": "Block validate fails before execution",
    "warn3": "Mining canceled because best chain already updated",
    "warn4": "cannot get block hash",
}

error_msgs = {
    "err1": "Error during discover",
    "err2": "Time slot already passed before execution",
    "err3": "Sender produced too many continuous blocks",
    "err4": "Execution cancelled",
    "err5": "Request chain 2113 failed"
}
