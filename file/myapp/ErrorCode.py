from enum import Enum

class ErrorCode(Enum):
    PARAMS_ERROR = (10001, "参数有误")
    ACCOUNT_PWD_NOT_EXIST = (10002, "用户名或密码不存在")
    ACCOUNT_EXIST = (10004, "账号已存在")
    NO_PERMISSION = (70001, "无访问权限")
    SESSION_TIME_OUT = (90001, "会话超时")
    NO_LOGIN = (90002, "未登录")
    REGISTRATION_FAILED=(1001,"注册失败，请稍后重试")
    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]
