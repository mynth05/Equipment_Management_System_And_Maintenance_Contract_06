from datetime import datetime, timedelta
from device import AirConditionRemote, Micro,  ProjectorRemote, DeviceStatus
from borrower import Lecturer, TeachingAssistant
from borrowing_slip import BorrowingSlip
from exceptions import BorrowingException

def run_tests():
    try:
        # 1. Tạo một giảng viên
        lecturer = Lecturer("GV01", "Nguyễn Văn A")
        print(f"-> Tạo giảng viên: {lecturer.borrower_name} (Tối đa {lecturer.get_maximum_devices()} thiết bị)")

        # 2. Tạo thiết bị
        projector_remote = ProjectorRemote("PR01", "Điều khiển máy chiếu", 2023, 500000)
        micro = Micro("MIC01", "Micro không dây", 2024, 1200000)
        air_condition_remote = AirConditionRemote("AC01", "Điều khiển điều hòa", 2022, 600000)
        print("-> Tạo thành công 3 thiết bị: PR01, MIC01, AC01.")

        # 3. Tạo phiếu mượn cho phòng học
        slip_date = datetime.now() - timedelta(days=5)
        slip = BorrowingSlip("SLIP01", lecturer, "Phòng 302", borrowed_date=slip_date)
        print(f"-> Tạo phiếu mượn {slip.slip_id} cho {slip.teaching_room}")

        # 4. Thêm thiết bị vào phiếu
        slip.add_device(projector_remote, borrow_days=3)  # Max 7 ngày
        slip.add_device(micro, borrow_days=1)          # Max 1 ngày
        print(f"-> Thêm thành công thiết bị vào phiếu. Tổng số lượng: {len(slip.items)}")

        # 5. Trả điều khiển máy chiếu đúng hạn
        return_date_proj = slip_date + timedelta(days=2)
        fee_proj = slip.return_device("PR01", return_date_proj)
        print(f"-> Trả PR01 đúng hạn. Phí phạt: {fee_proj} VND. Trạng thái mới: {projector_remote.status.value}")

        # 6. Trả micro muộn (hạn chót slip_date + 1 ngày, trả vào slip_date + 3 ngày)
        return_date_mic = slip_date + timedelta(days=3)
        fee_mic = slip.return_device("MIC01", return_date_mic)
        print(f"-> Trả MIC01 muộn. Phí phạt: {fee_mic} VND. Trạng thái mới: {micro.status.value}")

        print(f"-> Tổng phí trễ hạn toàn phiếu: {slip.calculate_total_late_fee()} VND")

    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")

    print("\n==============================================")
    print("       CHẠY CÁC LUỒNG PHÁT SINH NGOẠI LỆ")
    print("==============================================")

    # 1. Mượn điều khiển điều hòa đang UnderMaintenance
    print("\n[Test 1] Mượn thiết bị đang bảo trì (UnderMaintenance):")
    try:
        ac_broken = AirConditionRemote("AC99", "ĐH hỏng", 2021, 500000)
        ac_broken.status = DeviceStatus.UnderMaintenance
        ta = TeachingAssistant("TA01", "Trần Thị B")
        slip_ex1 = BorrowingSlip("SLIP_EX1", ta, "Phòng 101")
        slip_ex1.add_device(ac_broken, borrow_days=2)
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 2. Trợ giảng mượn thiết bị thứ 3 (Giới hạn tối đa là 2)
    print("\n[Test 2] Trợ giảng mượn vượt quá số lượng thiết bị cho phép:")
    try:
        ta2 = TeachingAssistant("TA02", "Lê Văn C")
        slip_ex2 = BorrowingSlip("SLIP_EX2", ta2, "Phòng 102")
        d1 = AirConditionRemote("AC11", "ĐH 1", 2023, 400000)
        d2 = AirConditionRemote("AC12", "ĐH 2", 2023, 400000)
        d3 = AirConditionRemote("AC13", "ĐH 3", 2023, 400000)
        slip_ex2.add_device(d1, 2)
        slip_ex2.add_device(d2, 2)
        slip_ex2.add_device(d3, 2)  # Vượt giới hạn
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 3. Thêm cùng một micro hai lần vào phiếu
    print("\n[Test 3] Thêm cùng một thiết bị hai lần vào phiếu:")
    try:
        lecturer2 = Lecturer("GV02", "Phạm Văn D")
        slip_ex3 = BorrowingSlip("SLIP_EX3", lecturer2, "Phòng 103")
        mic_dup = Micro("MIC22", "Micro trùng", 2023, 1000000)
        slip_ex3.add_device(mic_dup, 1)
        slip_ex3.add_device(mic_dup, 1)  # Trùng lặp
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 4. Mượn micro trong thời hạn lớn hơn giới hạn (Micro giới hạn tối đa 1 ngày)
    print("\n[Test 4] Thời hạn mượn lớn hơn giới hạn của thiết bị:")
    try:
        slip_ex4 = BorrowingSlip("SLIP_EX4", lecturer2, "Phòng 104")
        mic_limit = Micro("MIC33", "Micro 33", 2023, 1000000)
        slip_ex4.add_device(mic_limit, borrow_days=3)  # Vượt quá 1 ngày
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 5. Trả một thiết bị không thuộc phiếu mượn
    print("\n[Test 5] Trả thiết bị không thuộc phiếu mượn:")
    try:
        slip_ex5 = BorrowingSlip("SLIP_EX5", lecturer2, "Phòng 105")
        slip_ex5.return_device("PR_UNKNOWN", datetime.now())
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 6. Trả cùng một thiết bị hai lần
    print("\n[Test 6] Trả thiết bị đã được trả trước đó:")
    try:
        slip_ex6 = BorrowingSlip("SLIP_EX6", lecturer2, "Phòng 106")
        proj_ret = ProjectorRemote("PR22", "PJ 22", 2023, 800000)
        slip_ex6.add_device(proj_ret, 3)
        slip_ex6.return_device("PR22", datetime.now())
        slip_ex6.return_device("PR22", datetime.now())  # Trả lần 2
    except BorrowingException as ex:
        print(f"-> Bắt ngoại lệ thành công: {ex}")

    # 7. Trả thiết bị với ngày trả trước ngày mượn
    print("\n[Test 7] Ngày trả trước ngày mượn:")
    try:
        slip_ex7 = BorrowingSlip("SLIP_EX7", lecturer2, "Phòng 107")
        proj_date = ProjectorRemote("PR33", "PJ 33", 2023, 800000)
        slip_ex7.add_device(proj_date, 3)
        past_date = datetime.now() - timedelta(days=10)
        slip_ex7.return_device("PR33", past_date)
    except Exception as ex:
        print(f"-> Bắt ngoại lệ/lỗi thành công: {ex}")

if __name__ == "__main__":
    run_tests()