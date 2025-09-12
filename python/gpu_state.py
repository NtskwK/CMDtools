import pynvml

MB_UNIT = 1024 * 1024

def get_nv_state():
    """
    Retrieves the current state and statistics of all available NVIDIA GPUs using the pynvml library.
    Returns:
        dict: A dictionary containing the following keys:
            - "driver" (str): The NVIDIA driver version.
            - "count" (int): The number of detected GPU devices.
            - "devices" (list): A list of dictionaries, each representing a GPU device with the following keys:
                - "name" (str): The name of the GPU.
                - "index" (int): The index of the GPU.
                - "uuid" (str): The unique identifier of the GPU.
                - "driver_version" (str): The NVIDIA driver version.
                - "total_memory" (float): Total memory of the GPU in MB.
                - "used_memory" (float): Used memory of the GPU in MB.
                - "free_memory" (float): Free memory of the GPU in MB.
                - "temperature" (int): Current temperature of the GPU in Celsius.
                - "gpu_utilization" (int): Current GPU utilization percentage.
                - "memory_utilization" (int): Current memory utilization percentage.
                - "memory_free_rate" (float): Ratio of free memory to total memory.
    Raises:
        pynvml.NVMLError: If there is an error initializing, querying, or shutting down NVML.
    """

    pynvml.nvmlInit()

    info = dict()
    info["driver"] = pynvml.nvmlSystemGetDriverVersion()
    info["count"] = pynvml.nvmlDeviceGetCount()
    info["devices"] = []
    for i in range(info["count"]):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        gpu_temperature = pynvml.nvmlDeviceGetTemperature(handle, 0)
        gpuUtilRate = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        gpuMemoryRate = pynvml.nvmlDeviceGetUtilizationRates(handle).memory
        uuid = pynvml.nvmlDeviceGetUUID(handle)

        device_info = {
            "name": gpu_name,
            "index": i,
            "uuid": uuid,
            "driver_version": info["driver"],   
            "total_memory": memory_info.total / MB_UNIT,
            "used_memory": memory_info.used / MB_UNIT,
            "free_memory": memory_info.free / MB_UNIT,
            "temperature": gpu_temperature,
            "gpu_utilization": gpuUtilRate,
            "memory_utilization": gpuMemoryRate,
            "memory_free_rate": memory_info.free / memory_info.total
        }
        info["devices"].append(device_info)

    pynvml.nvmlShutdown()
    return info
