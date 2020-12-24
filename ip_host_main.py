#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

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

    def ip_location_by_qq_wry(self):
        """
        通过纯真IP数据库，将IP保存到CSV文件，文件名是IP的地理位置
        :return: None
        """
        # 获取index配置参数
        index = self._init_get_index.get_index_str()
        self._init_ip_location.make_ip_list(index)


if __name__ == '__main__':
    IPLocationHost().ip_host()
