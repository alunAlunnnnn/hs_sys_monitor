import click

from sys_monitor._get_sys_information import get_sys_info
from sys_monitor.utils._db_sqlite import SqliteDB


def _hard_info_parse(hard_info):
    fields, values = [], []

    # get cpu info
    cpu_info = hard_info.get("cpu_info")
    for field, value in cpu_info.items():
        fields.append(field)
        values.append(value)

    # get mem info
    mem_info = hard_info.get("mem_info")
    for field, value in mem_info.items():
        fields.append(field)
        values.append(value)

    # get disk info
    disk_info = hard_info.get("disk_info")
    fields.append("disk_info")
    values.append(str(disk_info).replace("'", '"'))

    # get unit info
    unit_info = hard_info.get("unit")
    fields.append("unit")
    values.append(unit_info)

    return fields, values


def _sys_status_parse(cpu_status, mem_status, disk_status):
    fields, values = [], []

    # get cpu info
    for field, value in cpu_status.items():
        fields.append(field)
        values.append(value)

    # get memory info
    for field, value in mem_status.items():
        fields.append(field)
        values.append(value)

    # get disk info
    fields.append("disk_io")
    values.append(str(disk_status).replace("'", '"'))

    return fields, values


def update_monitor_value_sqlite(db_file):
    """
    update tables in sqlite.
    :param db_file: sqlite db file
    :return:
    """
    # get system status and hardware info
    run_time, hard_info, cpu_status, mem_status, disk_status = get_sys_info()

    # init sqlite handler
    sqlite_handler = SqliteDB(db_file)

    # get target table
    t_hs_sys_monitor = sqlite_handler.get_table("t_hs_sys_monitor")
    t_hs_hard_info = sqlite_handler.get_table("t_hs_hard_info")

    # insert into hardware info table
    fields, values = _hard_info_parse(hard_info)
    fields.insert(0, "time")
    values.insert(0, run_time)
    t_hs_hard_info.insert(fields, values)

    # insert into system status table
    fields, values = _sys_status_parse(cpu_status, mem_status, disk_status)
    fields.insert(0, "time")
    values.insert(0, run_time)
    t_hs_sys_monitor.insert(fields, values)

    return "finish"


if __name__ == '__main__':
    update_monitor_value_sqlite("D:/systemonitor/example.db")
