from termcolor import colored

def parseText(text):
    t = ""
    for tt in text:
        t += str(tt) + ' '
    return t

class log:
    def ok(*text):
        text = parseText(text)
        print("      " + colored('[', attrs=['bold']) + colored('OK', 'green', attrs=['bold']) + colored(']', attrs=['bold']), "|", text)

    def error(*text):
        text = parseText(text)
        print("   " + colored('[', attrs=['bold']) + colored('ERROR', 'red', attrs=['bold']) + colored(']', attrs=['bold']), "|", text)

    def info(*text):
        text = parseText(text)
        print("    " + colored('[', attrs=['bold']) + colored('INFO', 'cyan', attrs=['bold']) + colored(']', attrs=['bold']), "|", text)

    def warn(*text):
        text = parseText(text)
        print(" " + colored('[', attrs=['bold']) + colored('WARNING', 'yellow', attrs=['bold']) + colored(']', attrs=['bold']), "|", text)
