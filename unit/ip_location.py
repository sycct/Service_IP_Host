#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from IPy import IP
import csv
import os
import platform

from . import load_qq_wry


class IPLocation:
    """
    查询纯真IP数据库，获取IP地址位置，并保存到CSV文件
    """

    def __init__(self):
        self._not_used_ip_range_prefix = [0, 10, 127, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236,
                                          237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
                                          252, 253, 254, 255]
        self._wry = load_qq_wry()

    def make_ip_list(self, index_str):
        # 0.0.0.0/8的IP总共是：16,777,216个IP地址
        # 当index=1,0到50
        start = (index_str - 1) * 50
        end = index_str * 50
        for item in range(start, end, 1):
            if item in self._not_used_ip_range_prefix:
                continue
            temp_list = []
            for index_str, ip in enumerate(IP(f'{item}.0.0.0/8')):
                temp_list.append(str(ip))
                if len(temp_list) > 100000 or index_str > 16700000:
                    self.multi_query_ip_location(temp_list)
                    temp_list.clear()

    def multi_query_ip_location(self, ip_list):
        for item in ip_list:
            ip = str(item)
            get_ip_str = self._wry.lookup(ip)
            if get_ip_str is None:
                return
            file_name = f"{get_ip_str[0]}_{get_ip_str[1]}.csv"
            platform_str = platform.system()
            if platform_str == 'Windows':
                file_path = os.path.join(os.getcwd(), f'files\\ip_location_csv\\{file_name}')
            else:
                file_path = os.path.join(os.getcwd(), f'files/ip_location_csv/{file_name}')
            self.write_ip_csv(file_path, [ip])

    @staticmethod
    def write_ip_csv(file_path, data):
        with open(file_path, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
