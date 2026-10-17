from typing import List, Optional
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod

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
        max_borrow_days: int,   # số ngày tối đa cho mượn
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
        self._status = DeviceStatus.Avaiable

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

    @status.setter
    def status(self, value = DeviceStatus):
        return self._status = value

    @property
    def max_borrow_days(self) -> int:
        return self._max_borrow_days

    @property
    def mark_as_borrowed(self):
        self._status = DeviceStatus.BORROWED

    def mark_as_available(self):
        self._status = DeviceStatus.AVAILABLE

    def __str__(self) -> str:
        return f"Device [{self._device_id}] - {self._name} | Trạng thái: {self._status.value} | Giá: {self._purchase_price}"

class AirConditionRemote (Device):
    def __init__ (
        self,
        device_id,
        device_name,
        year_of_use,
        purchase_price,
        status: DeviceStatus.Avaiable
    ):
        super().__init__(device_id, device_name, year_of_use, purchase_price,status)

    
