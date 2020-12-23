#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os


class GetIndex:
    """
    获取索引，每个服务器不同索引，方便大面积跑IP
    """

    def __init__(self):
        self._get_config_file = os.path.join(os.getcwd(), 'files/index.txt')

    def get_index_str(self):
        if os.path.exists(self._get_config_file):
            with open(self._get_config_file, 'r') as csv_file:
                # 文件存在，读取1行index
                index = int(csv_file.readline(1))
                return index
