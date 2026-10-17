from datetime import datetime, timedelta
from typing import List, Optional
from borrower import IBorrower
from device import Device, DeviceStatus
from borrow_item import BorrowItem
from exceptions import (
    DeviceUnavailableException,
    BorrowLimitExceededException,
    InvalidBorrowPeriodException,
    DuplicateDeviceException,
    DeviceNotInSlipException,
    DeviceAlreadyReturnedException
)

class BorrowingSlip:
    def __init__(self, slip_id: str, borrower: IBorrower, teaching_room: str, borrowed_date: Optional[datetime] = None):
        if not slip_id or not borrower or not teaching_room:
            raise ValueError("SlipId, Borrower và TeachingRoom phải hợp lệ.")
            
        self._slip_id = slip_id
        self._borrower = borrower
        self._teaching_room = teaching_room
        self._borrowed_date = borrowed_date or datetime.now()
        self._items: List[BorrowItem] = []

    @property
    def slip_id(self) -> str:
        return self._slip_id

    @property
    def borrower(self) -> IBorrower:
        return self._borrower

    @property
    def teaching_room(self) -> str:
        return self._teaching_room

    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date

    @property
    def items(self) -> List[BorrowItem]:
        return self._items

    def _validate_borrowing(self, device: Device, borrow_days: int):
        if device is None:
            raise ValueError("Thiết bị không được null.")
        if borrow_days <= 0 or borrow_days > device.max_borrow_days:
            raise InvalidBorrowPeriodException(device.device_id, borrow_days, device.max_borrow_days)
            
        # Kiểm tra trùng lặp thiết bị trong phiếu
        for item in self._items:
            if item.device.device_id == device.device_id:
                raise DuplicateDeviceException(device.device_id)
                
        # Kiểm tra giới hạn số thiết bị của người mượn
        if len(self._items) >= self._borrower.get_maximum_devices():
            raise BorrowLimitExceededException(self._borrower.borrower_id, self._borrower.get_maximum_devices())
            
        # Kiểm tra trạng thái thiết bị
        if device.status != DeviceStatus.Avaiable:
            raise DeviceUnavailableException(device.device_id, device.status.value)

    def add_device(self, device: Device, borrow_days: int):
        # Đảm bảo tính nhất quán: Kiểm tra toàn bộ điều kiện hợp lệ trước khi thay đổi trạng thái
        self._validate_borrowing(device, borrow_days)
        
        due_date = self._borrowed_date + timedelta(days=borrow_days)
        item = BorrowItem(device, self._borrowed_date, due_date)
        
        # Chỉ khi hợp lệ mới cập nhật trạng thái thiết bị và thêm vào danh sách
        device.mark_as_borrowed()
        self._items.append(item)

    def return_device(self, device_id: str, returned_date: datetime) -> float:
        if not device_id:
            raise ValueError("Mã thiết bị không hợp lệ.")
            
        target_item = None
        for item in self._items:
            if item.device.device_id == device_id:
                target_item = item
                break
                
        if target_item is None:
            raise DeviceNotInSlipException(device_id)
            
        if target_item.is_returned:
            raise DeviceAlreadyReturnedException(device_id)
            
        if returned_date < self._borrowed_date:
            raise ValueError("Ngày trả không được trước ngày mượn.")
            
        target_item.return_item(returned_date)
        target_item.device.mark_as_available()
        
        return self._calculate_late_fee_for_item(target_item, returned_date)

    def _calculate_late_fee_for_item(self, item: BorrowItem, returned_date: datetime) -> float:
        if returned_date > item.due_date:
            late_days = (returned_date - item.due_date).days
            return late_days * 10000.0  # Phí phạt ví dụ: 10,000 VND / ngày trễ
        return 0.0

    def calculate_total_late_fee(self) -> float:
        total = 0.0
        for item in self._items:
            if item.is_returned and item.returned_date and item.returned_date > item.due_date:
                late_days = (item.returned_date - item.due_date).days
                total += late_days * 10000.0
        return total