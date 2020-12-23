#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from qqwry import QQwry
import os


def load_qq_wry():
    wry = QQwry()
    ip_data_path = os.path.join(os.getcwd(), 'files\\qqwry.dat')
    if os.path.exists(ip_data_path):
        wry.load_file(ip_data_path, loadindex=True)
        return wry
