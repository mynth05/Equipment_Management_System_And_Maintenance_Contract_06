from datetime import datetime
from device import Device
from exceptions import DeviceAlreadyReturnedException

class BorrowItem:
    def __init__(self, device: Device, borrowed_date: datetime, due_date: datetime):
        if device is None:
            raise ValueError("Thiết bị không được null.")
        if due_date < borrowed_date:
            raise ValueError("DueDate phải sau hoặc bằng BorrowedDate.")
            
        self._device = device
        self._borrowed_date = borrowed_date
        self._due_date = due_date
        self._returned_date: datetime | None = None
        self._is_returned = False

    @property
    def device(self) -> Device:
        return self._device

    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @property
    def returned_date(self) -> datetime | None:
        return self._returned_date

    @property
    def is_returned(self) -> bool:
        return self._is_returned

    def return_item(self, returned_date: datetime):
        if self._is_returned:
            raise DeviceAlreadyReturnedException(self._device.device_id)
        if returned_date < self._borrowed_date:
            raise ValueError("Ngày trả không được trước ngày mượn.")
            
        self._returned_date = returned_date
        self._is_returned = True