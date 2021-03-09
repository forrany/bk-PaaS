#!/usr/bin/env python
# encoding: utf-8

import datetime

from django.utils import timezone

from common.log import logger
from common.constants import DATETIME_FORMAT_STRING


def parse_datetime(date_string, default, format=DATETIME_FORMAT_STRING):
    """
    转成datetime
    """
    if not date_string:
        return default
    try:
        dt = datetime.datetime.strptime(date_string, format)

        # from native time to local time
        current_tz = timezone.get_current_timezone()
        dt = current_tz.localize(dt)
    except Exception, e:
        logger.error("parse datetime fail! %s. [datetime=%s]" % (str(e), date_string))
        dt = default
    return dt


def get_time_delta(time_delta_string):
    """
    5m -> datetime.timedelta(minutes=5)
    5d -> datetime.timedelta(days=5)
    """
    count, _unit = time_delta_string[:-1], time_delta_string[-1]
    unit = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}.get(_unit, "minutes")
    return datetime.timedelta(**{unit: int(count)})


def _parse_datetime(date_string, format_string, zone=None, target_zone=None):
    """
    将不带时区的字符串转为目标时区的时间
    :param date_string:时间字符串
    :param format_string:时间字符串格式
    :param zone:时间字符串的时区，默认为本地时区
    :param target_zone: 目标时区，默认为本地时区
    """
    # get a naive datetime
    naive_dt = datetime.datetime.strptime(date_string, format_string)
    # makes a naive datetime.datetime in a given time zone aware.
    aware_dt = timezone.make_aware(naive_dt, zone)
    # converts an aware datetime.datetime to local time.
    target_aware_dt = timezone.localtime(aware_dt, target_zone)
    return target_aware_dt


def parse_local_datetime(date_string, format_string=DATETIME_FORMAT_STRING, zone=None):
    """
    将不带时区的字符串转为本地时区的时间
    :param date_string:时间字符串
    :param format_string:时间字符串格式
    :param zone:时间字符串的时区，默认为本地时区
    """
    return _parse_datetime(date_string, format_string, zone=zone)


def parse_utc_datetime(date_string, format_string=DATETIME_FORMAT_STRING, zone=None):
    """
    将不带时区的字符串转为UTC时区的时间
    :param date_string:时间字符串
    :param format_string:时间字符串格式
    :param zone:时间字符串的时区，默认为本地时区
    """
    return _parse_datetime(date_string, format_string, zone=zone, target_zone=timezone.utc)