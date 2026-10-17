from enum import Enum
from datetime import datetime

class DeviceStatus(Enum):
    Avaiable = "Avaiable"   # thiết bị có sẵn
    Borrowed = "Borrowed"   # thiết bị đã cho mượn
    UnderMaintenance = "UnderMaintainance"  #thiết bị đang bảo trì

class BorrowingException(Exception):
    """Ngoại lệ nghiệp vụ của cơ sở mượn trả"""
class Device():
    def __init__ (
        self,
        device_id: str, # mã thiết bị
        device_name: str,   # tên thiết bị
        year_of_use: int,   # năm đưa vào sử dụng
        purchase_price: float,   # giá mua
        max_borrow_days: int = 7,   # số ngày tối đa cho mượn
        status: DeviceStatus = DeviceStatus.Avaiable
    ):
        if not device_id or not device_id.strip():
           raise ValueError (" Mã thiết bị không được để trống.")
        if purchase_price <= 0:
            raise ValueError ("Giá mua phải lớn hơn 0.")
        if year_of_use > datetime.now().year:
            raise ValueError ("Năm đưa vào sửa dụng không được lớn hơn năm hiện tại.")

        self._device_id = str(device_id).strip()
        self._device_name = device_name
        self._year_of_use = year_of_use
        self._purchase_price = purchase_price
        self._max_borrow_days = max_borrow_days
        self._status = status

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def device_name(self) -> str:
        return self._device_name

    @property
    def year_of_use(self) -> int:
        return self._year_of_use

    @property
    def purcharse_price(self) -> float:
        return self._purchase_price

    @property
    def status(self) -> DeviceStatus:
        return self._status
    
    @status.setter
    def status(self, value: DeviceStatus):
        self._status = value

    @property
    def max_borrow_days(self) -> int:
        return self._max_borrow_days

    def mark_as_borrowed(self):
        self._status = DeviceStatus.Borrowed

    def mark_as_available(self):
        self._status = DeviceStatus.Avaiable

    def __str__(self) -> str:
        return f"Device [{self._device_id}] - {self.device_name} | Trạng thái: {self._status.value} | Giá: {self._purchase_price}"

class AirConditionRemote (Device):
    def __init__ (
        self,
        device_id,
        device_name,
        year_of_use,
        purchase_price
    ):
        super().__init__(device_id, device_name, year_of_use, purchase_price,max_borrow_days=5)

class Micro (Device):
    def __init__ (
        self,
        device_id,
        device_name,
        year_of_use,
        purchase_price
    ):
        super().__init__(device_id, device_name, year_of_use, purchase_price,max_borrow_days=1)

class ProjectorRemote (Device):
    def __init__ (
        self,
        device_id,
        device_name,
        year_of_use,
        purchase_price
    ):
        super().__init__(device_id, device_name, year_of_use, purchase_price,max_borrow_days=5)

    
