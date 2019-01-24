class SameError(Exception):
    def __init__(self, msg):
        self.msg = msg + '(이)가 중복입니다.'

    def __str__(self):
        return self.msg


class PasswordNotMatchError(Exception):
    def __init__(self):
        self.msg = '비밀번호와 비밀번호 확인이 다릅니다!'

    def __str__(self):
        return self.msg


class DoNotMatchWithTypeError(Exception):
    def __init__(self, msg):
        self.msg = msg + ' 사용자가 아닙니다!'

    def __str__(self):
        return self.msg
