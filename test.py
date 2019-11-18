import datetime

from analyzer import Analyzer

if __name__ == "__main__":
    # time转换并获取时间间隔
    start_str = '2019-11-13 08:56:14,976'
    end_str = '2019-11-18 06:12:58,995'
    start_time = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S,%f')
    end_time = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S,%f')
    days = (end_time - start_time).days
    seconds = (end_time - start_time).seconds
    timespan = 3600 * 24 * days + seconds
    blocks = 837061 - 2
    print('days: {0}'.format(days))
    print('seconds: {0}'.format(seconds))
    print('average blocks: {0}'.format(round(timespan/blocks, 3)))

    # 字典排序
    peer_info = {}
    peer_info["192.168.197.29:6801"] = 20
    peer_info["192.168.197.30:6801"] = 280
    peer_info["192.168.197.41:6801"] = 60
    peer_info["192.168.197.28:6801"] = 300
    peer_info["192.168.197.24:6801"] = 1000
    peer_info["192.168.197.26:6801"] = 240
    peer_info["192.168.197.32:6801"] = 15
    peer_info["192.168.197.22:6801"] = 27
    keys = sorted(peer_info.items(), key=lambda d: d[1])
    for item in keys:
        print("{0}, {1}".format(item[0], item[1]))

    analyzer = Analyzer("127.0.0.1:8000")
    analyzer.parse_network_hash("/Users/ericshu/Testing/logs/network-hash.log")
    analyzer.parse_network_peer("/Users/ericshu/Testing/logs/network-peer.log")
