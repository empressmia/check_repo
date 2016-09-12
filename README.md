# check_repo
Bash script for checking and updating git repositories named in a list if fast-forward is possible. Creates also a log file for retracing the repositories' status

## Usage
Uses own git alias! First type *git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'* into your terminal and hit enter. The command *git update* is explained by and used from [stackoverflow](http://stackoverflow.com/a/17101140).
Then make sure the script executable by running *chmod a+x check_repo.sh* and run it with *./check_repo.sh*.

## Remark
If you have no *repos.conf* file it will create one with an example path. You have to use full paths and no abbrivations! Just enter your paths to your repos into the .conf file and it will check and update all of them if possible, i.e. if merge with fast-forward is possible.
A new log file is created for each run of the script so one don't get a large unreadable file for all repos named in the list. If you want an ongoing log file though just comment line 36 out ('rm -f $log_file').
