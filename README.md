# check_repo
Bash script for checking and updating git repositories named in a list if fast-forward is possible. Creates also a log file for retracing the repositories' status. *autopush*, a new feature implemented, pushes commits automatically to remote on checked out branch (does not do any autocommit!).

## Usage
Uses own git alias! First type 

```bash
git config --global alias.update '!git remote update -p; git merge --ff-only @{u}'
```
 
into your terminal and hit enter. The command 
```bash
git update
``` 
is explained by and used from [stackoverflow](http://stackoverflow.com/a/17101140).
Then make sure the script is executable by running ```chmod a+x check_repo.sh``` and run it with ```./check_repo.sh```.
The following sections describe how to get a simpler usage for the script.

###Crontab
USE AT YOUR OWN RISK!
To run this script as a cron service at start up, add 
```
@reboot SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin /path/to/your/repo/check_repo/check_repo.sh
```
 to your crontab with typing ```crontab -e``` in your terminal.
For users using *archlinux* check [cron](https://wiki.archlinux.org/index.php/Cron) due to installation of cron services.

###Shell Alias
USE AT YOUR OWN RISK!
To run it as a shell command for the current user add a new alias to your *.bashrc* with ```sudo vim .bashrc```. Enter: 

```bash
alias checkrepos='/path/to/your/repo/check_repo/check_repo.sh'
```
Save and exit and source your bash file with ```. .bashrc``` or ```source .bashrc```

The script then can be called with ```checkrepos``` under the current user.
See [bash](https://wiki.archlinux.org/index.php/Bash#Configuration_files) for more information.

## Remarks
If you have no *repos.conf* file it will create one with an example path. You have to use full paths and no abbrivations! Just enter your paths to your repos into the *repos.conf* file and it will check and update all of them if possible, i.e. if merge with fast-forward is possible. It will also push local commits to remote if there are any.

A new log file is created for each run of the script so one don't get a large unreadable file for all repos named in the list. If you want an ongoing log file though just comment line 38 out ('```rm -f $log_file```').

# repo_manager
A python shell for managing your git-repostiories along with the bash script. Has autocompletion and history.

The shell has some commands one can list with hitting <kbd>Tab</kbd> twice, starting to type a command and hitting <kbd>Tab</kbd> once will autocomplete it.
Major feature is adding repositories to your *repos.conf* and managing it. If you add a new repo, the list will update itself. One can the actual log and the *workon <reponame>* command will open a new terminal with your repo path as working directory. Key idea was the possibility to quickly jump between repositories named on list.

Type *help* for all implemented commands with a short but useful description.

Currently the *gnome-terminal* is used to open a new terminal, using *workon*. Pleas feel free to enter the name of your terminal(-emulator) in line 222 in *repo_manager.py*. A configuration file for the shell will come by time.

### TODOs/Future Work
Only commands not implemented so far are *ignore* and *unignore* for keeping repositories on the watch-list, but excluding them from any autoupdate or autopush. Also comments to the source code will be added.
