#!/bin/sh
#author: RageQuitPepe
#              _      _    _        
#__ ____ _ _ _(_)__ _| |__| |___ ___
#\ V / _` | '_| / _` | '_ \ / -_|_-<
# \_/\__,_|_| |_\__,_|_.__/_\___/__/
#            
PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
config_file="$PWD/repos.conf"
log_file="$PWD/repo.log"
DATE=$(date)

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

#            _      
# _ __  __ _(_)_ _  
#| '  \/ _` | | ' \ 
#|_|_|_\__,_|_|_||_|
#                
if [ ! -e $config_file ]; then
    #creates template for repository list
    echo "No repo-list given!"
    echo "# _ _ ___ _ __  ___ ___" >> $config_file
    echo "#| '_/ -_) '_ \/ _ (_-<" >> $config_file
    echo "#|_| \___| .__/\___/__/" >> $config_file
    echo "#|       |_|           " >> $config_file
    echo "#----------------------"
    echo "#If you want a repository to be skipped just add '#' at the beginning of the line" >> $config_file
    echo "#Empty lines will be skipped too, so one can structure its list" >> $config_file
    echo "/full/path/to/your/repository" >> $config_file
    exit
else
    #delete existing log file
    rm -f $log_file
    echo "-------------------------------" | tee -a $log_file
    echo "Repository status for $DATE" | tee -a $log_file
    echo "-------------------------------" | tee -a $log_file
    #skip blank lines and lines starting with '#'
    sed -e '/^\s*$/ d' -e '/^#/ d' $config_file | while read repo; do
        #check if folder exists
	if [ -e $repo ]; then
		update=false
		push=false
		echo "$repo" | tee -a $log_file 
		cd "${repo}"
                #fetch is needed to check if a repository has changed
		git fetch | tee -a $log_file

		LOCAL=$(git rev-parse @)
		REMOTE=$(git rev-parse @{u})
		BASE=$(git merge-base @ @{u})
		COMMITS=$(git cherry -v @{u})

		#check is based on: http://stackoverflow.com/a/3278427
		if [ $LOCAL = $REMOTE ]; then
		    echo -e "${GREEN}Up-to-date${NC}"
		    echo "Up-to-date" >> $log_file
		elif [ $LOCAL = $BASE ]; then
		    echo -e "${ORANGE}Need to pull${NC}"
		    echo "Need to pull" >> $log_file
		    update=true
		#elif [ -z "$COMMITS" ]; then		
		elif [ $REMOTE = $BASE ]; then
                    push=true
		    echo -e "${BLUE}Need to push${NC}"
		    echo "Need to push" >> $log_file
		else
		    echo -e "${RED}Diverged${NC}"
		    echo "Diverged" >> $log_file
		fi

		#git update is explained by http://stackoverflow.com/a/17101140
		#i.e: git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'
		if $update ; then
			git update | tee -a $log_file
		fi
		if $push ; then
			#get checked out branch
			BRANCH="$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)"
			#push to remote for branch
			echo "Checked out branch is $BRANCH" | tee -a $log_file
			git push -u origin $BRANCH | tee -a $log_file
		fi
		echo "-------------------------------" | tee -a $log_file
	else
		echo -e "${RED}Repository $repo does not exist!${NC}"
		echo "Repository $repo does not exist!" >> $log_file
	fi
    done
fi
