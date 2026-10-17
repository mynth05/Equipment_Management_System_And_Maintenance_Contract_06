from typing import List
from enum import Enum
from datetime import datetime
class DeviceStatus(Enum):
    Avaiable = "Avaiable"   # thiết bị có sẵn
    Borrowed = "Borrowed"   # thiết bị đã cho mượn
    UnderMaintenance = "UnderMaintainance"  #thiết bị đang bảo trì

class Device():
    def __init__ (
        self,
        device_id: str, # mã thiết bị
        device_name: str,   # tên thiết bị
        year_of_use: int,   # năm đưa vào sử dụng
        purchase_price: float,   # giá mua
        status: DeviceStatus = DeviceStatus.Avaiable # trạng thái hoạt động
    ):
        if not device_id or not device_id.strip():
           raise ValueError (" Mã thiết bị không được để trống.")
        if purchase_price <= 0:
            raise ValueError ("Giá mua phải lớn hơn 0.")
        if year_of_use > datetime.now().year:
            raise ValueError ("Năm đưa vào sửa dụng không được lớn hơn năm hiện tại.")
        
