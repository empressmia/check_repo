#
# repo-management install Makefile
#

DEST_REPOMANAGER = /usr/local/bin/gitmanager
DEST_UPDATEREPOS = /usr/local/bin/updaterepos

executable:
	@echo "#!/bin/sh\n" > gitmanager.sh
	@echo "python $(CURDIR)/repo_manager.py\n" >> gitmanager.sh
	@echo "#!/bin/sh\n" > updaterepos.sh
	@echo "sh $(CURDIR)/check_repo.sh\n" >> updaterepos.sh

gitalias:
	@git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'

install:
	@echo "May need sudo rights to invoke!"
	@make gitalias
	@make executable
	@chmod +x $(CURDIR) check_repo.sh
	@chmod +x $(CURDIR) repo_manager.py
	@chmod a+x $(CURDIR) gitmanager.sh
	@chmod a+x $(CURDIR) updaterepos.sh
	@cp -p $(CURDIR)/gitmanager.sh $(DEST_REPOMANAGER)
	@cp -p $(CURDIR)/updaterepos.sh $(DEST_UPDATEREPOS)
	@echo "Installation complete"

clean:
	@rm $(DEST_REPOMANAGER)
	@rm $(CURDIR)gitmanager.sh 
	@rm $(CURDIR) repos.conf
	@rm $(CURDIR) repo_manager.conf

