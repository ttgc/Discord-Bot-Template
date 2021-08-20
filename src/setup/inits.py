#!usr/bin/env python3
#-*-coding:utf-8-*-

import logging, os
from src.setup.config import *

class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG+1

def initlogs():
    config = Config()["logs"]
    if not os.access(config["directory"], os.F_OK):
        os.mkdir(config["directory"])
    logger = logging.getLogger('discord')
    logging.basicConfig(level=logging.DEBUG+1)

    # basic handler (all)
    if config["all"]["enabled"]:
        logmode = 'a' if config["all"]["stacking"] else 'w'
        logfile = "{}/{}".format(config["directory"], config["all"]["filename"])
        handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode=logmode)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    # latest logs
    if config["latest"]["enabled"]:
        logmode = 'a' if config["latest"]["stacking"] else 'w'
        logfile = "{}/{}".format(config["directory"], config["latest"]["filename"])
        handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode=logmode)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

    # error logs
    if config["errors"]["enabled"]:
        logmode = 'a' if config["errors"]["stacking"] else 'w'
        logfile = "{}/{}".format(config["directory"], config["errors"]["filename"])
        handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode=logmode)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)

    # debug logs
    if config["debug"]["enabled"]:
        logmode = 'a' if config["debug"]["stacking"] else 'w'
        logfile = "{}/{}".format(config["directory"], config["debug"]["filename"])
        handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode=logmode)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        handler.addFilter(DebugFilter())
        logger.addHandler(handler)

    return logger
