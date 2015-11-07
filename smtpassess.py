__author__ = 'Yavor-Nb'

from os.path import dirname, basename, isfile
import glob
import sys, time
import ConfigParser
import mail_access
import datetime
from logger import Logger

USAGE_STRING = """
Usage: smtpassess <hostname> (port)
"""

WAIT_TIME = 30

testers = []
configuration = None
target = None
logger = None
access = None

def print_banner(hostname):
    logger.log(0, "---------------------------------------------------------  +")
    logger.log(2, "Started smtpassess")
    logger.log(2, "Target: " + hostname)
    logger.log(2, "Start time: " + str(datetime.datetime.now()))

def perform_tests():
    for tester in testers:
        tester.perform_tests(target)

def collect_results():
    for tester in testers:
        tester.check_results(access)

def load_plugins():
    modules = []
    loaded_plugins = []
    sys.path.append(dirname(__file__)+"plugins/")
    search_path = dirname(__file__)+"plugins/*.py"
    plugin_files = glob.glob(search_path)
    for plugin in plugin_files:
        try:
            if isfile(plugin):
                module_name = basename(plugin)[:-3]
                modules.append(__import__(module_name))
                loaded_plugins.append(module_name)
        except RuntimeError as er:
            print er
    for module in modules:
        testers.append(module.tester(logger, configuration))
    logger.log(1, "Loaded plugins: " + ",".join(loaded_plugins))

def read_configuration():
    global configuration
    configuration = ConfigParser.ConfigParser()
    configuration.read("config.ini")
    logger.log(2, "Loaded configuration file")

def main():
    global access, logger, target
    if len(sys.argv) < 2:
        print USAGE_STRING
        sys.exit(0)
    hostname = sys.argv[1]
    port = 25
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    target = (hostname, port)
    logger = Logger()
    print_banner(hostname)
    read_configuration()
    load_plugins()
    access = mail_access.MailAccess(configuration)
    logger.log(2, "Starting the tests")
    perform_tests()
    # Wait for processing before attempting to collect results
    logger.log(2, "Waiting for server processing of mails")
    time.sleep(WAIT_TIME)
    collect_results()

if __name__=="__main__":
    main()