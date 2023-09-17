from django.http import JsonResponse,HttpResponse
class Result:
    def __init__(self, success, code, msg, data):
        self.success = success
        self.code = code
        self.msg = msg
        self.data = data
    def to_dict(self):
        return {
            'success': self.success,
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }
    @staticmethod
    def success(data):
        return JsonResponse(Result(True, 200, "success", data).to_dict())

    @staticmethod
    def fail(code, msg):
        return JsonResponse(Result(False, code, msg, None).to_dict())