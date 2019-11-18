import datetime

if __name__ == "__main__":
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
