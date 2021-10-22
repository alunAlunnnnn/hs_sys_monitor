import psutil
import time
import json
from functools import lru_cache


@lru_cache(60)
def get_hrad_info(start_time):
    # print("func get_hrad_info")
    hard_info = {}
    # get cpu info
    cpu_count_logical = psutil.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)

    # get disk info
    disk_info = _get_disk_capacity(start_time)
    hard_info["disk_info"] = disk_info
    hard_info["unit"] = "GB"

    # save all infos
    hard_info["cpu_info"] = {
        "cpu_logical": cpu_count_logical,
        "cpu_physical": cpu_count_physical
    }

    # get ram info
    mem_info = _get_mem_status(start_time)
    hard_info["mem_info"] = {
        "mem_total": mem_info.get("mem_total"),
        "mem_use_size": mem_info.get("mem_use_size"),
        "mem_free": mem_info.get("mem_free"),
        "swap_total": mem_info.get("swap_total"),
        "swap_use_size": mem_info.get("swap_total"),
        "swap_free": mem_info.get("swap_total")
    }

    return hard_info


@lru_cache(60)
def _get_cpu_status(start_time):
    # print("func _get_cpu_status")
    cpu_status = {}

    cpu_use = psutil.cpu_percent(interval=1, percpu=True)
    # get cpu use maximum
    cpu_use_max = max(cpu_use)
    # get cpu use average
    cpu_use_avg = sum(cpu_use) / cpu_use.__len__()

    cpu_use_json = {}
    for i, each_cpu_use in enumerate(cpu_use):
        cpu_use_json[f"cpu_{i}"] = each_cpu_use

    cpu_status["cpu_use_avg"] = round(cpu_use_avg, 2)
    cpu_status["cpu_use_max"] = round(cpu_use_max, 2)
    cpu_status["cpu_use_percore"] = json.dumps(cpu_use_json)

    return cpu_status


@lru_cache(60)
def _get_mem_status(start_time):
    # print("func _get_mem_status")
    mem_status = {}

    # RAM, unit is bytes
    mem = psutil.virtual_memory()
    # virtual RAM
    swap = psutil.swap_memory()

    mem_status["mem_total"] = _byte_convert(mem.total, "gb")
    mem_status["mem_use"] = mem.percent
    mem_status["mem_use_size"] = _byte_convert(mem.used, "gb")
    mem_status["mem_free"] = _byte_convert(mem.free, "gb")

    mem_status["swap_total"] = _byte_convert(swap.total, "gb")
    mem_status["swap_use"] = swap.percent
    mem_status["swap_use_size"] = _byte_convert(swap.used, "gb")
    mem_status["swap_free"] = _byte_convert(swap.free, "gb")

    mem_status["unit"] = "gb"

    return mem_status


@lru_cache(60)
def _get_disk_net_status(start_time):
    # print("func _get_disk_status")
    disk_status_res = {}

    # get disk read/write capacity with dict type
    disk_io_origin = psutil.disk_io_counters(perdisk=True)
    net_io_origin = psutil.net_io_counters()
    time.sleep(1)
    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters(perdisk=True)

    # calculate disk io per second
    for disk_name, disk_status in disk_io_origin.items():
        # read/write capacity
        read_bytes_origin, write_bytes_origin = disk_status.read_bytes, disk_status.write_bytes
        read_bytes, write_bytes = disk_io[disk_name].read_bytes, disk_io[disk_name].write_bytes

        read_io = read_bytes - read_bytes_origin
        write_io = write_bytes - write_bytes_origin
        # disk_status_res[disk_name] = {"read": read_io, "write": write_io}
        unit = "mb"
        disk_status_res[disk_name] = {
            "read": _byte_convert(read_io, "mb"),
            "write": _byte_convert(write_io, "mb"),
            "unit": unit
        }

    # network i/o and package i/o
    net_status = _net_io_calculate(net_io_origin, net_io)

    return disk_status_res, net_status


def _net_io_calculate(net_io_origin, net_io):
    net_send = _byte_convert(net_io.bytes_sent - net_io_origin.bytes_sent, "m")
    net_receive = _byte_convert(net_io.bytes_recv - net_io_origin.bytes_recv, "m")
    net_package_send = net_io.packets_sent - net_io_origin.packets_sent
    net_package_receive = net_io.packets_recv - net_io_origin.packets_recv

    net_status = {
        "net_send": net_send,
        "net_receive": net_receive,
        "net_package_send": net_package_send,
        "net_package_receive": net_package_receive
    }

    return net_status


@lru_cache(60)
def _get_disk_capacity(time):
    # print("func _get_disk_capacity")
    disk_status = {}
    # only get local disk
    disks = psutil.disk_partitions(all=False)
    for each_disk in disks:
        disk = psutil.disk_usage(each_disk.mountpoint)
        disk_status[each_disk.mountpoint] = {
            "total": _byte_convert(disk.total, "gb"),
            "used": _byte_convert(disk.used, "gb"),
            "free": _byte_convert(disk.free, "gb"),
            "use": disk.percent,
            "unit": "gb"
        }

    return disk_status


@lru_cache(60)
def _byte_convert(bytes, target_type):
    target_type = target_type.lower().strip()
    if target_type in ("k", "kb", "kilobyte"):
        res = bytes / 1024
    elif target_type in ("m", "mb", "megabyte"):
        res = bytes / 1024 ** 2
    elif target_type in ("g", "gb", "gigabyte"):
        res = bytes / 1024 ** 3
    else:
        res = "Not Support"

    return round(res, 2)


def get_sys_info():
    start = time.time()
    # print("start: ", start)

    # get hard info and update table
    hard_info = get_hrad_info(start)
    # print(hard_info)

    # get system status info and insert into table
    cpu_status = _get_cpu_status(start)
    mem_status = _get_mem_status(start)
    disk_status, net_status = _get_disk_net_status(start)
    # print("cpu status: ", cpu_status)
    # print("mem status: ", mem_status)
    # print("disk status: ", disk_status)

    # finish = time.time()
    # print("finish: ", finish)

    # cost = finish - start
    # print("cost: ", cost)

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)), hard_info, cpu_status, mem_status, disk_status, net_status


if __name__ == '__main__':
    get_sys_info()
