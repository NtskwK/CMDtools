import psutil

MB_UNIT = 1024 * 1024
GB_UNIT = 1024 * MB_UNIT


def get_system_state():
    """
    Collects and returns the current system state information including CPU usage, memory, swap, and disk statistics.

    Returns:
        dict: A dictionary containing the following keys:
            - "cpu_percent" (float): The current CPU usage percentage.
            - "memory" (dict): Memory statistics with keys:
                - "total" (float): Total physical memory in MB.
                - "used" (float): Used physical memory in MB.
                - "free" (float): Free physical memory in MB.
                - "percent" (float): Percentage of memory used.
            - "swap" (dict): Swap memory statistics with keys:
                - "total" (float): Total swap memory in GB.
                - "used" (float): Used swap memory in GB.
                - "free" (float): Free swap memory in GB.
                - "percent" (float): Percentage of swap used.
            - "disk" (dict): Disk usage statistics for the root directory with keys:
                - "total" (float): Total disk space in GB.
                - "used" (float): Used disk space in GB.
                - "free" (float): Free disk space in GB.
                - "percent" (float): Percentage of disk used.

    Note:
        Requires the `psutil` library and the constants `MB_UNIT` and `GB_UNIT` to be defined.
    """
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    cpu_percent = psutil.cpu_percent(interval=1)
    info = dict()
    info["cpu_percent"] = cpu_percent
    info["memory"] = {
        "total": memory.total / MB_UNIT,
        "used": memory.used / MB_UNIT,
        "free": memory.free / MB_UNIT,
        "percent": memory.percent,
    }
    info["swap"] = {
        "total": swap.total / MB_UNIT,
        "used": swap.used / MB_UNIT,
        "free": swap.free / MB_UNIT,
        "percent": swap.percent,
    }
    info["disk"] = {
        "total": disk.total / MB_UNIT,
        "used": disk.used / MB_UNIT,
        "free": disk.free / MB_UNIT,
        "percent": disk.percent,
    }
    return info


if __name__ == "__main__":
    print(get_system_state())
