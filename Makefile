#
# repo-management install Makefile
#

SHELL = /bin/sh

DEST_DIR = /usr/local/bin/repo_manager
CURRENT_DIR = $(CURDIR)

test:
	cd $(DEST_DIR)
	echo $(CURRENT_DIR)

install:
	mkdir -p $(DEST_DIR)
	cp -uv $(CURRENT_DIR)/check_repo.sh $(DEST_DIR)/
	cp -uv $(CURRENT_DIR)/repo_manager.py repo_manager.py $(DEST_DIR)/
	chmod +x $(DEST_DIR)/check_repo.sh
	chmod +x $(DEST_DIR)/repo_manager.py

	
