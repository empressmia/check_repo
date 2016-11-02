#
# repo-management install Makefile
#

DEST_REPOMANAGER = /usr/bin/gitmanager
DEST_CHECKREPO = /usr/bin/checkrepo
CURRENT_DIR = $(CURDIR)

install:
	@echo "May need sudo rights to invoke!"
	@chmod +x $(DEST_DIR) check_repo.sh
	@chmod +x $(DEST_DIR) repo_manager.py
	@ln -s $(CURRENT_DIR)/check_repo.sh $(DEST_CHECKREPO)
	@ln -s $(CURRENT_DIR)/repo_manager.py $(DEST_REPOMANAGER)
	@echo "Installation complete"

clean:
	@rm $(DEST_REPOMANAGER)
	@rm $(DEST_CHECKREPO)
	
