#
# repo-management install Makefile
#

DEST_REPOMANAGER = /usr/local/bin/gitmanager

executable:
	@echo "#!/bin/sh\n" > gitmanager.sh
	@echo "python $(CURDIR)/repo_manager.py\n" >> gitmanager.sh

gitalias:
	@git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'

install:
	@echo "May need sudo rights to invoke!"
	@make gitalias
	@make executable
	@chmod +x $(CURDIR) check_repo.sh
	@chmod +x $(CURDIR) repo_manager.py
	@chmod a+x $(CURDIR) gitmanager.sh
	@cp -p $(CURDIR)/gitmanager.sh $(DEST_REPOMANAGER)
	@echo "Installation complete"

clean:
	@rm $(DEST_REPOMANAGER)
	@rm $(CURDIR)gitmanager.sh 
	@rm $(CURDIR) repos.conf
	@rm $(CURDIR) repo_manager.conf

