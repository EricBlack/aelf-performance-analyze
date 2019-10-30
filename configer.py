#! /usr/bin/python3
import sys
from configparser import ConfigParser


class ConfigInfo(object):
    LogPath = ''
    Endpoint = ''
    Start = 0
    End = 0
    Online = False

    def get_config(self):
        params = sys.argv
        if len(params) != 5:
            raise Exception('wrong parameters, four parameters needed.')

        section = params[1]
        start = int(params[2])
        end = int(params[3])
        online = str2bool(params[4])
        config = read_config(section)
        self.LogPath = config['log_path']
        self.Endpoint = config['endpoint']
        if start > end:
            raise Exception('start height should be bigger than end height.')
        self.Start = start
        self.End = end
        self.Online = online

        return self


config_instance = ConfigInfo()


def read_config(section):
    cfg = ConfigParser()
    cfg.read('config.ini')
    sections = cfg.sections()
    if section not in sections:
        raise Exception('wrong config section name')
    log_path = cfg.get(section, 'log_path')
    endpoint = cfg.get(section, 'endpoint')

    return {
        'log_path': log_path,
        'endpoint': endpoint
    }


def str2bool(info):
    if info in ['true', 'TRUE', 'True', 'y', 'Y']:
        return True
    return False
