#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from unit import ip_host, ip_location, get_index


class IPLocationHost:
    """
    获取IP的地理位置，以及HostName
    """

    def __init__(self):
        self._init_host = ip_host.IPHost()
        self._init_ip_location = ip_location.IPLocation()
        self._init_get_index = get_index.GetIndex()

    def ip_host(self):
        """
        更具IP地址，获取HostName并保存到csv文件
        :return: None
        """
        # 获取index配置参数
        index = self._init_get_index.get_index_str()
        self._init_host.make_ip_list(index)

    def ip_host_missing_ip_range(self):
        # 补充中间缺失部分IP地址
        self._init_host.missing_ip_range()

    def ip_host_other_ip_range(self):
        # 由于单个服务器运行十分慢，所以分一部分IP地址给其他服务器运行
        self._init_host.other_ip_range()

    def ip_location_by_qq_wry(self):
        """
        通过纯真IP数据库，将IP保存到CSV文件，文件名是IP的地理位置
        :return: None
        """
        # 获取index配置参数
        index = self._init_get_index.get_index_str()
        self._init_ip_location.make_ip_list(index)

    def process_error_ip_location_by_qq_wry(self):
        # 查询地址，执行中程序错误，中断部分
        self._init_ip_location.make_int_ip_list()
        # 执行程序错误，剩余部分
        self._init_ip_location.temp_ip_list()


if __name__ == '__main__':
    IPLocationHost().ip_host_missing_ip_range()
