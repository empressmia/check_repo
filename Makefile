#
# repo-management install Makefile
#

DEST_REPOMANAGER = /usr/local/bin/gitmanager
#DEST_CHECKREPO = /usr/local/bin/checkrepo

executable:
	@echo "#!/bin/sh\n" > gitmanager.sh
	@echo "python $(CURDIR)/repo_manager.py\n" >> gitmanager.sh

gitalias:
	@git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'

install:
	@echo "May need sudo rights to invoke!"
	@chmod +x $(CURDIR) check_repo.sh
	@chmod +x $(CURDIR) repo_manager.py
	@chmod +x $(CURDIR) gitmanager.sh
	@cp $(CURDIR)/gitmanager.sh $(DEST_REPOMANAGER)
	@echo "Installation complete"

clean:
	@rm $(DEST_REPOMANAGER)
	@rm $(DEST_CHECKREPO)
	@rm $(CURDIR) gitmanager.sh repos.conf repo_manager.conf

