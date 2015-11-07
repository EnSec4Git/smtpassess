__author__ = 'Yavor-Nb'

class Logger:
    def __init__(self):
        pass

    def log(self, level, logstring):
        prefix = "+ "
        if level == 1: # Verbose
            prefix += "(V)"
        elif level == 2: # Info
            prefix += "(INFO)"
        elif level == 3: # Warning
            prefix += "(WARN)"
        elif level == 4: # Error
            prefix += "(ERROR)"
        prefix += " "
        lines = logstring.split('\n')
        for line in lines:
            print prefix + line