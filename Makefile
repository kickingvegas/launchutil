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

INSTALL_DIR=$(HOME)/bin
EXEC_NAME=launchutil

.PHONY: help install

$(INSTALL_DIR):
	mkdir $(INSTALL_DIR)

install: $(INSTALL_DIR)
	cp -f $(EXEC_NAME).py $(INSTALL_DIR)/$(EXEC_NAME)
	chmod uog+x $(INSTALL_DIR)/$(EXEC_NAME)

uninstall:
	rm $(INSTALL_DIR)/$(EXEC_NAME)

help: base-help \
create-help \
install-help \
uninstall-help \
bootstrap-help \
bootout-help \
reload-help \
enable-help \
disable-help \
print-help


base-help:
	./$(EXEC_NAME).py -h

create-help:
	./$(EXEC_NAME).py create -h

install-help:
	./$(EXEC_NAME).py install -h

uninstall-help:
	./$(EXEC_NAME).py uninstall -h

bootstrap-help:
	./$(EXEC_NAME).py bootstrap -h

bootout-help:
	./$(EXEC_NAME).py bootout -h

reload-help:
	./$(EXEC_NAME).py reload -h

enable-help:
	./$(EXEC_NAME).py enable -h

disable-help:
	./$(EXEC_NAME).py disable -h

print-help:
	./$(EXEC_NAME).py print -h

test1:
	./$(EXEC_NAME).py create \
--working-directory . \
--program saytime.sh \
--daily 9:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00 17:00 \
--execute \
com.yummymelon.saytime 


