#!/usr/bin/python
#author: RageQuitPepe
#shell with autocompletion w. and w/o. history is based on: https://pymotw.com/2/readline/ which was cited at: http://stackoverflow.com/a/7821956
#Registering ctrl+c as exit-command is explained here: http://stackoverflow.com/a/1112350


#  _                     _
# (_)_ __  _ __  ___ _ _| |_ ___
# | | '  \| '_ \/ _ \ '_|  _(_-<
# |_|_|_|_| .__/\___/_|  \__/__/
#         |_|

import signal
import sys
import readline
import logging
import os
import subprocess
import time

#   __ _ _
#  / _(_) |___ ___
# |  _| | / -_|_-<
# |_| |_|_\___/__/

LOG = '/tmp/log.log'
HISTORY = '/tmp/completer.hist'
CONFIG = os.path.dirname(os.path.abspath(__file__))+'/repos.conf'
#CONFIG = os.path.dirname(os.path.abspath(__file__))
REPOMANAGER_CONFIG = os.path.dirname(os.path.abspath(__file__))+'/repo_manager.conf'
#REPOMANAGER_CONFIG = os.path.dirname(os.path.abspath(__file__))
REPO_LOG_DIR = os.path.dirname(os.path.abspath(__file__))+'/log'
REPO_LOG = os.path.dirname(os.path.abspath(__file__))+'/log/repo.log'
CHECK = os.path.dirname(os.path.abspath(__file__))+'/check_repo.sh'
#CHECK = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=LOG,level=logging.DEBUG)
#LOAD_CONFIG = os.path.join(CONFIG, 'repos.conf')
#LOAD_MANAGERCONFIG = os.path.join(REPOMANAGER_CONFIG, 'repo_manager.conf')
#LOAD_CHECKER = os.path.join(CHECK, 'check_repo.sh')


#       _     _          _
#  __ _| |___| |__  __ _| |___
# / _` | / _ \ '_ \/ _` | (_-<
# \__, |_\___/_.__/\__,_|_/__/
# |___/


REPOSITORIES = dict()
ENTRY_REPO_LIST = dict()
commands = ['exit', 'help', 'list', 'addrepo', 'removerepo', 'ignore', 'unignore', 'savelog', 'showlog', 'updaterepos', 'getpath', 'workon']
repositories = []
terminal = 'gnome-terminal'

#     _
#  __| |__ _ ______ ___ ___
# / _| / _` (_-<_-</ -_|_-<
# \__|_\__,_/__/__/\___/__/
class Completer(object):
    def __init__(self,options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
                logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
                logging.debug('(empty input) matches: %s', self.matches)

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s',
                      repr(text), state, repr(response))
        return response

def get_history_items():
    return [ readline.get_history_item(i)
             for i in range(1, readline.get_current_history_length() + 1)
             ]

class HistoryCompleter(object):

    def __init__(self):
        self.matches = []
        return

    def complete(self, text, state):
        if state == 0:
            history_values = get_history_items()
            logging.debug('history: %s', history_values)
            if text:
                self.matches = sorted(h
                                      for h in history_values
                                      if h and h.startswith(text))
            else:
                self.matches = []
            logging.debug('matches: %s', self.matches)
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s',
                      repr(text), state, repr(response))
        return response
#            _   _            _
#  _ __  ___| |_| |_  ___  __| |___
# | '  \/ -_)  _| ' \/ _ \/ _` (_-<
# |_|_|_\___|\__|_||_\___/\__,_/__/

def help():
    print("            Helpscreen of repo-manager:           ")
    print("--------------------------------------------------")
    print("List of available commands:                     \n")
    print(" - exit               : quits program             ")
    print(" - workon     [OPTION]: work in git repository    ")
    print("                      : name of repo              ")
    print(" - showgraph  [OPTION]: show graph of repository  ")
    print("                      : name of repo              ")
    print(" - addrepo    [OPTION]: adds repository to list   ")
    print("                      : /full/path/to/repo        ")
    print(" - removerepo [OPTION]: removes repo from list    ")
    print("                      : name of repo              ")
    print(" - getpath    [OPTION]: returns path of named repo")
    print("                      : name of repo              ")
    print(" - ignore     [OPTION]: ignore repo               ")
    print("                      : name of repo              ")
    print(" - unignore   [OPTION]: unignore repo             ")
    print("                      : name of repo              ")
    print(" - updaterepos        : updates repos in list     ")
    print(" - list               : lists active repositories ")
    print(" - savelog            : saves current log         ")
    print(" - showlog            : prints status log       \n")
    print("Usage examples:                                   ")
    print("addrepo /home/username/cool_project_repo          ")
    print("ignore cool_project_repo                          ")

def closing_message():
    print("Thanks for using the repo-manager, have a nice day!")

def get_repo_array():
	global REPOSITORIES
	global repositories
	if len(REPOSITORIES)>0:
		for key in REPOSITORIES.keys():
			repositories.append(key)
	return repositories

def start_up():
    print(" _ __ ___ _ __   ___ ______ _ __ ___   __ _ _ __   __ _  __ _  ___ _ __ ")
    print("| '__/ _ \ '_ \ / _ \______| '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|")
    print("| | |  __/ |_) | (_) |     | | | | | | (_| | | | | (_| | (_| |  __/ |   ")
    print("|_|  \___| .__/ \___/      |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|   ")
    print("         | |                                             __/ |          ")
    print("         |_|                                            |___/           ")
    print("\n")
    print("by RageQuitPepe")
    print("\n")

def compare_dicts():
    global REPOSITORIES
    global ENTRY_REPO_LIST
    entryKeySet = set(ENTRY_REPO_LIST.keys())
    actualKeySet = set(REPOSITORIES.keys())
    entryValueSet = set(ENTRY_REPO_LIST.values())
    actualValueSet = set(REPOSITORIES.values())
    if len(entryKeySet.difference(actualKeySet))>0 or len(entryValueSet.difference(actualValueSet))>0 or len(ENTRY_REPO_LIST.keys()) != len(REPOSITORIES.keys()) or len(ENTRY_REPO_LIST.values()) != len(REPOSITORIES.values()):
        difference = True
    else:
        difference = False

    return difference

def update_config(updateConfig):
    global REPOSITORIES
    if len(REPOSITORIES.values())>0:
        if updateConfig:
            print("WARNING: repositories have changed, updating config file!")
            with open(CONFIG, 'w') as fp:
                fp.write("#  _ _ ___ _ __  ___ ___ \n")
                fp.write("# | '_/ -_) '_ \/ _ (_-< \n")
                fp.write("# |_| \___| .__/\___/__/ \n")
                fp.write("#        |_|             \n")
            fp.close()
            for value in REPOSITORIES.values():
                with open(CONFIG, 'a') as fp:
                    fp.write(value+"\n")
                fp.close()
    else:
        print("ERROR: Repositories have changed but something went wrong... not udpating list!")


def scan_config():
	tmp_lines = []
	if os.path.isfile(CONFIG):
		with open(CONFIG, "r") as fp:
		    tmp_lines = list(line for line in (l.strip() for l in fp) if line)
		fp.close()

	else:
		print("Repository list does not exist, creating empty template!")
		with open(CONFIG, 'w') as fp:
			fp.write("#  _ _ ___ _ __  ___ ___ \n")
			fp.write("# | '_/ -_) '_ \/ _ (_-< \n")
			fp.write("# |_| \___| .__/\___/__/ \n")
			fp.write("#        |_|             \n")
			fp.write("/path/to/your/repo       \n")
		fp.close()

	return tmp_lines
		

def get_repository_list():
    global REPOSITORIES
    repoList = scan_config()
    for repo in repoList:
        if repo.startswith("#"):
            repo = repo[1:]
        if os.path.exists(repo):
            REPOSITORIES[os.path.basename(os.path.normpath(repo))] = repo

def list_repos():
    global REPOSITORIES
    if len(REPOSITORIES.keys()) > 0:
        for key in REPOSITORIES.keys():
            print(key)
    else:
        print("WARNING: Your repository list seems to be empty or does not have any valid paths")

def repo_log():
    with open(REPO_LOG) as fp:
        lines = list(line for line in (l.strip() for l in fp) if line)
        for line in lines:
            print (line)

def update_repos():
    update_config(compare_dicts())
    subprocess.call(CHECK)

def remove_repo(removeRepo):
    global REPOSITORIES
    if os.path.basename(os.path.normpath(removeRepo)) in REPOSITORIES:
        del REPOSITORIES[os.path.basename(os.path.normpath(removeRepo))]
    else:
        print("WARNING: Repository was not named in list, nothing to do...")

def work_on(repo):
    if repo in REPOSITORIES:
        subprocess.call(terminal+' --working-directory=' + '%s' % get_path_of_repo(repo), shell=True)

def add_repo(repository):
    global REPOSITORIES
    addRepo = False
    if os.path.exists(repository):
        os.chdir(repository)
        if os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
            if not os.path.basename(os.path.normpath(repository)) in REPOSITORIES:
                    addRepo = True
            else:
                print("WARNING: Repository already added to list!")
        else:
            print("ERROR: Named directory is not a git repository!")
    else:
        print("ERROR: Directory does not exist!")

    if addRepo:
        REPOSITORIES[os.path.basename(os.path.normpath(repository))] = repository

def get_path_of_repo(repoName):
    global REPOSITORIES
    if repoName in REPOSITORIES:
        return REPOSITORIES[repoName]
    else:
        return "WARNING: Repository not in list!"

def save_log():
    if os.path.isfile(REPO_LOG):
        subprocess.call(['cp %s %s' % (REPO_LOG, REPO_LOG_DIR+'/repo_log_'+time.strftime("%d_%m_%Y")+'.log')], shell=True)
    else:
        print("ERROR: No log file exists!")

def signal_handler(signal, frame):
	closing_message()
	sys.exit(0)

def check_repomanager_conf():
	global terminal
	if os.path.isfile(REPOMANAGER_CONFIG):
		with open(REPOMANAGER_CONFIG, "r") as fp:
			tmp_lines = list(line for line in (l.strip() for l in fp) if line)
		fp.close()
	
		terminal = tmp_lines[0]
	else:
		with open(REPOMANAGER_CONFIG, "w") as fp:
			fp.write(terminal+"\n")
		fp.close

def entry_loop():
    if os.path.exists(HISTORY):
        readline.read_history_file(HISTORY)
    try:
        while True:
			
            line = raw_input('$: ')
            tokens = line.split()

            if len(tokens) > 0 and len(tokens) <= 2:
                if len(tokens) == 1:
                    command = tokens[0]
                    option = ''
                if len(tokens) == 2:
                    command = tokens[0]
                    option = tokens[1]
            else:
                command = ''
                option = ''

            if command == 'exit':
                break
            elif command == 'help' or command == '':
                help()
            elif command == 'list':
                list_repos()
            elif command == 'addrepo':
                if option != '' :
                    add_repo(option)
                else:
                    print("ERROR: No valid option given!")
            elif command == 'removerepo':
                remove_repo(option)
            elif command == 'ignore':
                print("$: Sorry, not yet implemented")
            elif command == 'unignore':
                print("$: Sorry, not yet implemented")
            elif command == 'showlog':
                repo_log()
            elif command == 'savelog':
                save_log()
            elif command == 'updaterepos':
                update_repos()
            elif command == 'getpath':
                if option != '':
                    print(get_path_of_repo(option))
            elif command == 'workon':
                if option != '':
                    work_on(option)
            else:
                line = raw_input('$: ')

    finally:
        readline.write_history_file(HISTORY)


#             _
#  _ __  __ _(_)_ _
# | '  \/ _` | | ' \
# |_|_|_\__,_|_|_||_|
#

REPOSITORIES.clear()
ENTRY_REPO_LIST.clear()
get_repository_list()
ENTRY_REPO_LIST = REPOSITORIES.copy()

get_repo_array()
check_repomanager_conf()
start_up()
readline.set_completer(Completer(commands+repositories).complete)
readline.parse_and_bind('tab: complete')
signal.signal(signal.SIGINT, signal_handler)

entry_loop()
update_config(compare_dicts())
closing_message()
