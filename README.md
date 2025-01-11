# Git-Management
*Bash* and *Python* scripts for checking and updating git repositories named in a list if merging with fast-forward is possible. Creates also a log file for retracing the repositories' status. *autopush*, a new feature implemented, pushes commits automatically to remote on checked out branch (does not do any autocommit!).
The Python-script lets you manage the shell-script so that one can add new repositories on the watch list and let's you quickly work in your repos via your favourite-terminal. The python script is just an commandline-addition to the shell-script. The shell-script works stand-alone without the python-script but not vice versa.

## Installation
Just run `make install` and the Makefile will create executable copies to the scripts in this git repository as *gitmanager* and as *updterepos*. Both scripts are then systemwide callable. The needed git-alias for the shell-script is also set using the Makefile.
To set up your terminal for the *gitmanager*, edit the *repo_manager.toml* and enter the name of your terminal emulator (See descriptions at section *repo_manager*).

### Crontab
USE AT YOUR OWN RISK!
To run the shell-script as a cron service at start up, add 
```
@reboot SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin /path/to/your/repo/check_repo/check_repo.sh
```
 to your crontab with typing ```crontab -e``` in your terminal.
For users using *archlinux* check [cron](https://wiki.archlinux.org/index.php/Cron) due to installation of cron services.

## Remarks
If you have no *repos.conf* file it will create one with an example path. You have to use full paths and no abbreviations! Just enter your paths to your repos into the *repos.conf* file and it will check and update all of them if possible, i.e. if merge with fast-forward is possible. It will also push local commits to remote if there are any.

A new log file is created for each run of the script so one don't get a large unreadable file for all repos named in the list. If you want an ongoing log file though just comment line 38 out ('```rm -f $log_file```').

# repo_manager
A *Python* shell for managing your git-repostiories along with the bash script. Has autocompletion and command history.

The shell has some commands one can list with hitting <kbd>Tab</kbd> twice. Starting to type a command and hitting <kbd>Tab</kbd> once will autocomplete it (will also auto-complete names of listed repositories).
Major feature is adding repositories to your *repos.conf* and managing it. If you add a new repo, the list will update itself. One can save the actual log and the *workon <reponame>* command will open a new terminal with your repo path as working directory. Key idea was the possibility to quickly jump between repositories named on the list.

Type *help* for all implemented commands with a short description.

##### NEW
The `repo_manager` has now a own config-file called `repo_manger.toml` which is automatically
created after a first execution. Change the value for keyword `terminal` to the name of the terminal emulator you use. The default one is `konsole`. Also
an empty repository-list is created after the first run (which should also be a bugfix if you haven't run the shell-script first, sorry for that inconvenience).

