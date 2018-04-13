import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')


class PlcService:
    """
    PLCとのやり取りを行う
    PLC Serverからの要求はコマンドライン上で受取るため、直接Model等が呼べない。
    そのためWeb-API経由で呼び出している
    """
    def __init__(self):
        self.web_api_server = "127.0.0.1:8000"


    def receive_plc_message(self, data):
        print("HEY!!! {}".format(data))
        print("Will Send to %s" % self.web_api_server)

