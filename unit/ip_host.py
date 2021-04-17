#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
from IPy import IP
import csv
import os
from concurrent import futures
import IPy
import requests
from requests import exceptions

from config import LoggingConfig


class IPHost:
    """
    通过IP获取Host name,并保存到scv文件
    """

    def __init__(self):
        self._init_log = LoggingConfig().init_logging('Host_IP')
        self._save_country_file = os.path.join(os.getcwd(), 'files/host.csv')
        self._max_workers = 50
        # 私有IP地址，排除
        self._not_used_ip_range_prefix = [0, 10, 127, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236,
                                          237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
                                          252, 253, 254, 255]

    def make_ip_list(self, index_str):
        # 总共是：16,777,216个IP地址
        # 当index=1,0到50
        start = (index_str - 1) * 50
        end = index_str * 50
        self.traverse_ip_range(start, end)

    def missing_ip_range(self):
        # 中间缺失IP地址查询rDNS
        start = IPy.IP('200.111.216.10').int()
        end = IPy.IP('224.0.0.0').int()
        temp_list = []
        for int_ip in range(start, end, 1):
            # 将int ip装换成ip形式，加入到列表
            temp_list.append(IPy.intToIp(int_ip, version=4))
            # 队列100,000条数据开始循环，同时避免最后几条无法循环
            if len(temp_list) > 100000 or int_ip > 3758073002:
                self.query_many_by_google_dns(temp_list)
                temp_list.clear()

    def other_ip_range(self):
        # 由于单个服务器循很慢，所以从1-50 IP段又分出10-50IP段，给其他服务器运行
        start = 10
        end = 50
        self.traverse_ip_range(start, end)

    def traverse_ip_range(self, start, end):
        # 循环IP段，注意：必须是/8结尾的，否则程序会出错或者有些IP地址没有跑
        for item in range(start, end, 1):
            if item in self._not_used_ip_range_prefix:
                continue
            temp_list = []
            for index_str, ip in enumerate(IP(f'{item}.0.0.0/8')):
                temp_list.append(ip)
                if len(temp_list) > 100000 or index_str > 16700000:
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

    def query_many_by_google_dns(self, ip_list):
        with futures.ThreadPoolExecutor(self._max_workers) as executor:
            to_do = []
            for item in ip_list:
                future = executor.submit(self.get_host_by_google_dns, str(item))
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

    def get_host_by_google_dns(self, ip):
        ip = IP(ip)
        reverse_name = ip.reverseName()
        uri = f"https://dns.google/resolve?name={reverse_name}&type=PTR"
        try:
            get_result = requests.get(uri, timeout=5)
        except (exceptions.ConnectionError, exceptions.HTTPError, exceptions.Timeout) as e:
            self._init_log.error(f"网络出现错误，具体错误内容：{e}")
            return False
        result_json = get_result.json()
        try:
            get_answer = result_json['Answer'][0]
        except KeyError:
            self._init_log.error(f"{ip},没有找到Answer。")
            return False
        get_type = get_answer['type']
        if get_type == 12:
            # 转换成域名形式
            host = get_answer['data'][0:-1]
        try:
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
