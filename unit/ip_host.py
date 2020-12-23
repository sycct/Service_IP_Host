#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
from IPy import IP
import csv
import os
from concurrent import futures

from config import LoggingConfig


class IPHost:
    """
    通过IP获取Host name,并保存到scv文件
    """

    def __init__(self):
        self._init_log = LoggingConfig().init_logging('Host_IP')
        self._save_country_file = os.path.join(os.getcwd(), 'files/host.csv')
        self._max_workers = 1000
        # 私有IP地址，排除
        self._not_used_ip_range_prefix = [0, 10, 127, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236,
                                          237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
                                          252, 253, 254, 255]

    def make_ip_list(self, index_str):
        # 总共是：16,777,216个IP地址
        # 当index=1,0到50
        start = (index_str - 1) * 50
        end = index_str * 50
        for item in range(start, end, 1):
            if item in self._not_used_ip_range_prefix:
                continue
            temp_list = []
            for index_str, ip in enumerate(IP(f'{item}.0.0.0/8')):
                temp_list.append(ip)
                if len(temp_list) > 100000 or index_str > 167:
                    self.query_many(ip_list=temp_list)
                    temp_list.clear()

    def query_many(self, ip_list):
        with futures.ThreadPoolExecutor(self._max_workers) as executor:
            to_do = []
            for item in ip_list:
                future = executor.submit(self.get_host, str(item))
                to_do.append(future)

                results = []
                for future in futures.as_completed(to_do):
                    res = future.result()
                results.append(res)
        return len(results)

    def get_host(self, ip):
        try:
            # 判断是bot，获取IP
            host = socket.gethostbyaddr(ip)[0]
            host_ip = socket.gethostbyname(host)
        except (socket.herror, socket.error, socket.gaierror, UnicodeError) as e:
            # 验证失败，应该记录错误，以方便以后处理问题
            self._init_log.error(f'通过IP解析Host的时候出现错误，错误内容：{e},IP地址：{ip}')
            return False
        if host_ip == ip:
            # 如果验证通过，加入search_engine_bot_ip列表,之后显示正常页面
            self.write_csv_file([ip, host])

    def write_csv_file(self, data):
        with open(self._save_country_file, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
