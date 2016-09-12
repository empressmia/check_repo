# check_repo
Bash script for checking and updating git repositories named in a list if fast-forward is possible. Creates also a log file for retracing the repositories' status

## Usage
First make the script executable by running *chmod a+x check_repo.sh*. If you have no *repos.conf* file it will create one with an example path. You have to use full paths and no abbrivations!

A new log file is created for each run of the script so one don't get a large unreadable file for all repos named in the list. If you want an ongoing log file though just comment line 36 out ('rm -f $log_file').
