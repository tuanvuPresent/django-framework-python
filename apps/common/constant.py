from enum import Enum


class ErrorMessage(Enum):
    def __new__(cls, code, message):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.message = message
        return obj

    UNKNOWN_ERROR = (10001, 'Đã có lỗi xảy ra, vui lòng thử lại')
    INVALID_AUTH = (10002, 'Xác thực không hợp lệ')
    NOT_AUTH = (10003, 'Cần đăng nhập để sử dụng chức năng này')
    NOT_PERMISSION = (10004, 'Bạn không có quyền thực hiện hành động này')
    THROTTLED_REQUEST = (
        10005, 'Quyền truy cập bị hạn chế, có thể bạn đã đưa ra quá nhiều yêu cầu vào lúc này')
    NOT_FOUND = (10006, 'Không tìm thấy bản ghi')
    NOT_ALLOW_METHOD = (10007, 'Phương thức này không cho phép')
    LOGIN_FAIL = (10008, 'Tên đăng nhập hoặc mật khẩu không đúng')
    FORMAT_FILE = (10009, 'Định dạng file không hợp lệ')
    RESET_PASSWORD_TOKEN_INVALID = (
        10010, 'Mã khôi phục mật khẩu không hợp lệ')
    RESET_PASSWORD_CODE_INVALID = (
        100011, 'Mã khôi phục mật khẩu không hợp lệ')
    EMAIL_REQUIRED = (10012, 'Email nhân viên không được để trống')
    PASSWORD_REQUIRED = (10014, 'Mật khẩu không được để trống')
    RESET_PASSWORD_CODE_REQUIRED = (10015, 'Mã khôi phục không được để trống')
    EMAIL_NOT_EXIST = (10016, 'Email không tồn tại')
    LINK_RESET_PASS_INVALID = (10017, 'Đường dẫn không hợp lệ hoặc đã hết hạn')
    TOKEN_REQUIRED = (10018, 'Mã khôi phục không được để trống')
    UID_REQUIRED = (10019, 'Mã ngưởi dùng không được để trống')
