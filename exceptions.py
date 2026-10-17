# Hệ thống ngoại lệ nghiệp vụ
class BorrowingException(Exception):
    """Ngoại lệ cơ sở cho hệ thống mượn thiết bị."""
    def __init__(self, message, inner_exception=None):
        super().__init__(message)
        self.inner_exception = inner_exception


class DeviceUnavailableException(BorrowingException):
    """Phát sinh khi thiết bị không ở trạng thái Available."""
    def __init__(self, device_id: str, current_status: str):
        super().__init__(f"Thiết bị '{device_id}' không ở trạng thái sẵn sàng. Trạng thái hiện tại: {current_status}.")
        self.device_id = device_id
        self.current_status = current_status


class BorrowLimitExceededException(BorrowingException):
    """Phát sinh khi người mượn đã đạt số thiết bị tối đa."""
    def __init__(self, borrower_id: str, maximum_devices: int):
        super().__init__(f"Người mượn '{borrower_id}' đã đạt giới hạn tối đa cho phép là {maximum_devices} thiết bị.")
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices


class InvalidBorrowPeriodException(BorrowingException):
    """Phát sinh khi số ngày mượn không dương hoặc lớn hơn giới hạn của thiết bị."""
    def __init__(self, device_id: str, requested_days: int, max_allowed_days: int):
        super().__init__(f"Thời hạn mượn {requested_days} ngày không hợp lệ cho thiết bị '{device_id}' (Giới hạn tối đa: {max_allowed_days} ngày).")
        self.device_id = device_id
        self.requested_days = requested_days
        self.max_allowed_days = max_allowed_days


class DuplicateDeviceException(BorrowingException):
    """Phát sinh khi cùng một thiết bị đã tồn tại trong phiếu."""
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị '{device_id}' đã tồn tại trong phiếu mượn này.")
        self.device_id = device_id


class DeviceNotInSlipException(BorrowingException):
    """Phát sinh khi yêu cầu trả một thiết bị không thuộc phiếu mượn."""
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị '{device_id}' không thuộc phiếu mượn này.")
        self.device_id = device_id


class DeviceAlreadyReturnedException(BorrowingException):
    """Phát sinh khi thiết bị trong phiếu đã được trả trước đó."""
    def __init__(self, device_id: str):
        super().__init__(f"Thiết bị '{device_id}' đã được trả trước đó rồi.")
        self.device_id = device_id