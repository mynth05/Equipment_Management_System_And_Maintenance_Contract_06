from typing import List, Optional
from device import Device
from device import DeviceStatus

class ClassRoom:
    def __init__(self, room_id: str, room_name: str, capacity: int):
        self._room_id = room_id
        self._room_name = room_name
        self._capacity = capacity
        self._devices: List[Device] = []

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def room_name(self) -> str:
        return self._room_name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def devices(self) -> List[Device]:
        return self._devices

    def add_device(self, device: Device):
        if device is None:
            raise ValueError("Không chấp nhận đối tượng thiết bị null.")
        if self.find_device(device.device_id) is not None:
            raise ValueError(f"Thiết bị có mã {device.device_id} đã tồn tại trong phòng.")
        self._devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        device = self.find_device(device_id)
        if device:
            self._devices.remove(device)
            return True
        return False

    def find_device(self, device_id: str) -> Optional[Device]:
        for d in self._devices:
            if d.device_id == device_id:
                return d
        return None

