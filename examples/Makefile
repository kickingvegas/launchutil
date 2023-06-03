# Copyright 2023 Charles Y. Choi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

SAYTIME_SERVICE=com.yummymelon.saytime
EXEC_NAME=launchutil

.PHONY: clean \
install_and_load_saytime \
install_saytime \
bootstrap_saytime \
uninstall_saytime \
print_saytime

$(SAYTIME_SERVICE).plist:
	$(EXEC_NAME) create \
--program saytime.sh \
--daily 9:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00 17:00 \
--execute \
com.yummymelon.saytime

install_and_load_saytime: install_saytime bootstrap_saytime

install_saytime: $(SAYTIME_SERVICE).plist
	$(EXEC_NAME) install --execute $(SAYTIME_SERVICE)

bootstrap_saytime:
	$(EXEC_NAME) bootstrap --execute $(SAYTIME_SERVICE)

uninstall_saytime:
	$(EXEC_NAME) bootout --execute $(SAYTIME_SERVICE)
	$(EXEC_NAME) uninstall --execute $(SAYTIME_SERVICE)

print_saytime:
	$(EXEC_NAME) print --execute $(SAYTIME_SERVICE)

clean:
	rm $(SAYTIME_SERVICE).plist
