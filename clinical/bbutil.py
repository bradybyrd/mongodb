#  BB lib - Python Helper
import datetime
import json
import os
import sys
import subprocess
import pprint

class Util:
    def __init__(self, details = {}):
        self.secrets = []
        self.logfile = False
        self.logfilename = "run_log.txt"
        self.hfile = False
        if "secrets" in details:
            self.secrets = secrets
        if "file" in details:
            self.logfile = True

        self.somthin = "more"

    def init_log():
        self.logit("#------------- New Run ---------------#")

    def set_details(self, details):
        if "secrets" in details:
            self.secrets = secrets
        if "file" in details:
            self.logfile = True

    def add_secret(self, item):
        self.secrets.append(str(item))

    def logit(self, message, log_type = "INFO", display_only = True):
        cur_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        stamp = f"{cur_date}|{log_type}> "
        if type(message) == dict or type(message) == list:
            message = str(message)
        self.file_log(message)
        if log_type == "raw":
            message = "Raw output, check file"
        for line in message.splitlines():
            cleaned = self.sanitize(line)
            print(f"{stamp}{cleaned}")

    def message_box(self, msg, mtype = "sep"):
        tot = 100
        start = ""
        res = ""
        msg = msg[0:84] if len(msg) > 85 else msg
        ilen = tot - len(msg)
        if (mtype == "sep"):
            start = f'#{"-" * int(ilen/2)} {msg}'
            res = f'{start} {"-" * (tot - len(start) + 1)}#'
        else:
            res = f'#{"-" * tot}#\n'
            start = f'#{" " * int(ilen/2)} {msg} '
            res += f'{start}{" " * (tot - len(start) + 1)}#\n'
            res += f'#{"-" * tot}#\n'

        self.logit(self.sanitize(res))
        return res

    def sanitize(self, txt):
        cleaned = str(txt).strip()
        for item in self.secrets:
            cleaned = cleaned.replace(item, "*******")
        return cleaned

    def run_shell(self, cmd = ["ls", "-l"]):
        self.logit(f'Running: {" ".join(cmd)}')
        result = subprocess.run(cmd, capture_output=True)
        self.logit("The exit code was: %d" % result.returncode)
        self.logit("#--------------- STDOUT ---------------#")
        self.logit(result.stdout)
        if result.stderr:
            self.logit("#--------------- STDERR ---------------#")
            self.logit(result.stderr)
        return result

    def separator(self, ilength = 102):
        dashy = "-" * (ilength - 2)
        self.logit(f'#{dashy}#')

    def print_timer(self, starttime):
        elapsed = datetime.datetime.now() - starttime
        self.logit(f'Elapsed time: {str(elapsed)}')

    def process_args(self, arglist):
        args = {}
        for arg in arglist:
            pair = arg.split("=")
            if len(pair) == 2:
                args[pair[0].strip()] = pair[1].strip()
            else:
                args[arg] = ""
        return args

    def read_json(self, json_file, is_path = True):
        result = {}
        if is_path:
            with open(json_file) as jsonfile:
                result = json.load(jsonfile)
        else:
            result = json.loads(json_file)
        return result

    def save_json(self, json_file, data, is_path = True):
        if is_path:
            with open(json_file, 'w') as outfile:
                json.dump(data, outfile)
        else:
            result =json.dump(data, outfile)

    def file_log(self, content, action = "none"):
        if not self.logfile:
            return("goody")
        if action == "new":
            ver = self.logfilename.split(".")[0].replace("run_log","")
            inc = 1 if ver == "" else int(ver) + 1
            self.logfilename = f"run_log{inc}.txt"
        cur_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        stamp = f"{cur_date}|I> "
        with open(self.logfilename, 'a') as lgr:
            lgr.write(f'{stamp}{content}\n')
