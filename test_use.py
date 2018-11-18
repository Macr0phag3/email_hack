# -*- coding: utf-8 -*-

import FakeEmail

test = FakeEmail.FakeEmail(from_addr="hr@361.com", to_addr="15619047890@163.com")
print test.attack("hello! my friend!", "hr: you got it!")
