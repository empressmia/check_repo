#!/usr/bin/python3.5
#author: RageQuitPepe
#shell with autocompletion w. and w/o. history is based on: https://pymotw.com/2/readline/ which was cited at: http://stackoverflow.com/a/7821956


#  _                     _
# (_)_ __  _ __  ___ _ _| |_ ___
# | | '  \| '_ \/ _ \ '_|  _(_-<
# |_|_|_|_| .__/\___/_|  \__/__/
#         |_|

import readline
import logging
import os
import subprocess

#   __ _ _
#  / _(_) |___ ___
# |  _| | / -_|_-<
# |_| |_|_\___/__/

LOG = '/tmp/log.log'
HISTORY = '/tmp/completer.hist'
CONFIG = './repos.conf'
REPO_LOG = './log/repo.log'
CHECK = './check_repo.sh'
logging.basicConfig(filename=LOG,level=logging.DEBUG)
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
    print(" - addrepo    [OPTION]: adds repository to list   ")
    print("                      : /full/path/to/repo        ")
    print(" - removerepo [OPTION]: removes repo from list    ")
    print("                      : name of repo              ")
    print(" - ignore     [OPTION]: ignore repo               ")
    print("                      : name of repo              ")
    print(" - unignore   [OPTION]: unignore repo             ")
    print("                      : name of repo              ")
    print(" - run                : updates repos in list     ")
    print(" - list               : lists active repositories ")
    print(" - savelog            : saves current log         ")
    print(" - showlog            : prints status log       \n")
    print("Usage examples:                                   ")
    print("addrepo /home/username/cool_project_repo          ")
    print("ignore cool_project_repo                          ")

def closing_message():
    print("Thanks for using the repo-manager, have a nice day!")

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

def scan_config():
    with open(CONFIG) as fp:
        tmp_lines = list(line for line in (l.strip() for l in fp) if line)
    fp.close()
    return tmp_lines

def list_repos():
    with open(CONFIG) as fp:
        lines = list(line for line in (l.strip() for l in fp) if line)
        for line in lines:
            if line.startswith("#"):
                line = line[1:]
            if os.path.exists(line):
                print (line)

def repo_log():
    with open(REPO_LOG) as fp:
        lines = list(line for line in (l.strip() for l in fp) if line)
        for line in lines:
            print (line)

def update_repos():
     subprocess.call("./"+CHECK)

def add_repo(repository):
    addRepo = True
    if os.path.exists(repository):
        os.chdir(repository)
        if os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
            for line in scan_config():
                if line.startswith("#"):
                    line = line[1:]
                if line == repository:
                    print ("WARNING: Repository already added to list!")
                    addRepo = False
        else:
            print("ERROR: Named directory is not a git repository!")
    else:
        print("ERROR: Directory does not exist!")
    if addRepo:
        with open(CONFIG, 'a') as fp:
            fp.write(repository)
        fp.close()


def entry_loop():
    if os.path.exists(HISTORY):
        readline.read_history_file(HISTORY)
    try:
        while True:

            line = input('$: ')
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
            if command == 'help' or command == '':
                help()
            if command == 'list':
                list_repos()
            if command == 'addrepo':
                print("WARNING: Does not yet work properly!")
                if option != '' :
                    add_repo(option)
                else:
                    print("ERROR: No valid option given!")
            if command == 'removerepo':
                print("$: Sorry, not yet implemented")
            if command == 'ignore':
                print("$: Sorry, not yet implemented")
            if command == 'unignore':
                print("$: Sorry, not yet implemented")
            if command == 'showlog':
                repo_log()
            if command == 'savelog':
                print("$: Sorry, not yet implemented")
            if command == 'run':
                update_repos()

    finally:
        readline.write_history_file(HISTORY)


#             _
#  _ __  __ _(_)_ _
# | '  \/ _` | | ' \
# |_|_|_\__,_|_|_||_|
#

start_up()
readline.set_completer(Completer(['exit', 'help', 'list', 'addrepo', 'removerepo', 'ignore', 'unignore', 'savelog', 'showlog', 'run']).complete)
readline.parse_and_bind('tab: complete')

entry_loop()
closing_message()