#
# repo-management install Makefile
#

DEST_REPOMANAGER = /usr/bin/gitmanager
DEST_CHECKREPO = /usr/bin/checkrepo

gitalias:
	@git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'

install:
	@echo "May need sudo rights to invoke!"
	@make gitalias
	@chmod +x $(CURDIR) check_repo.sh
	@chmod +x $(CURDIR) repo_manager.py
	@ln -s $(CURDIR)/check_repo.sh $(DEST_CHECKREPO)
	@ln -s $(CURDIR)/repo_manager.py $(DEST_REPOMANAGER)
	@echo "Installation complete"

clean:
	@rm $(DEST_REPOMANAGER)
	@rm $(DEST_CHECKREPO)

reinstall:
	make clean
	make install	
