#  Copyright 2024 Medicines Discovery Catapult
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

def fake_response(code: int, body: dict = None):
    def side_effect(*args, **kwargs):
        class Resp:
            def __init__(self, c: int, b: dict = None):
                self.status_code = c
                self.body = b
                self.content = 'fake'

            def json(self):
                return self.body

        return Resp(code, body)
    return side_effect
