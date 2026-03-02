import datetime
import json
import os
from endstone.command import Command, CommandSender
from endstone.plugin import Plugin
from endstone import ColorFormat, Player

class CatSign(Plugin):
    api_version = "0.10"
    authors = ["XinYueNeko"]

    def __init__(self):
        super().__init__()
        """ Money """
        data_dir = os.path.join(os.getcwd(), "plugins", "CatSign")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        conf_data_file = os.path.join(data_dir, "config.json")
        if not os.path.exists(conf_data_file):
            with open(conf_data_file, "w", encoding='utf-8') as f:
                cf_data = {
                    "money": "50",
                    "title": "签到插件"
                }
                json_str = json.dumps(cf_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(conf_data_file, "r", encoding='utf-8') as f:
                cf_data = json.load(f)
        self.cf_data = cf_data
        self.data_dir = data_dir

    commands = {
        "qd" : {
            "description": "签到命令",
            "usages": ["/qd"],
            "permissions": ["neko.qd.cmd.qd"]
        }
    }

    permissions = {
        "neko.qd.cmd.qd": {
            "description": "签到命令",
            "default": True
        }
    }

    def on_load(self):
        self.logger.info(f"{ColorFormat.AQUA}CatSign loading...")

    def on_enable(self):
        if not self.server.plugin_manager.get_plugin("ye111566_jsonmoney"):
            self.logger.info(f"{ColorFormat.RED}没有JsonMoney经济插件,")
            self.logger.info(f"{ColorFormat.RED}CatSign Disabling...")
            self.server.plugin_manager.disable_plugin(self)
        else:
            self.logger.info(f"{ColorFormat.AQUA}CatSign is Enabled!{ColorFormat.RESET}")
            self.logger.info(f"{ColorFormat.AQUA}Author: {ColorFormat.RESET}XinYueNeko")

    def on_disable(self):
        self.logger.info(f"{ColorFormat.AQUA}CatSign is Disabled!{ColorFormat.RESET}")

    def on_command(self, sender: CommandSender, cmd: Command, args: list[str])->bool:
        """ JsonMoney """
        jsonmoney = self.server.plugin_manager.get_plugin("ye111566_jsonmoney")
        """ Y-M-D """
        mstr = self.cf_data.get("money") #获取str : money
        qz = self.cf_data.get("title") #获取插件前缀
        mi = int(mstr) #读取Json的int
        u = sender.name
        ny = datetime.datetime.now().year
        nm = datetime.datetime.now().month
        nd = datetime.datetime.now().day
        tm_data = os.path.join(self.data_dir, f"{nm}-{nd}-{ny}")
        tm_data_json = os.path.join(tm_data, f"{u}.json")
        if isinstance(sender, Player):
            match cmd.name:
                case "qd":
                    if not os.path.exists(tm_data):
                        os.makedirs(tm_data)
                        with open(os.path.join(tm_data, tm_data_json), "w", encoding='utf-8') as f:
                            f.write("Time")
                        jsonmoney.change(u, mi)
                        sender.send_message(f"{ColorFormat.AQUA}[{qz}]{ColorFormat.WHITE}签到成功, 获得{mi}块钱!")
                    elif not os.path.exists(tm_data_json):
                        with open(tm_data_json, "w", encoding='utf-8') as f:
                            f.write("{\"Time\":\"\"}")
                        jsonmoney.change(u, mi)
                        sender.send_message(f"{ColorFormat.AQUA}[{qz}]{ColorFormat.WHITE}签到成功, 获得{mi}块钱!")
                    elif os.path.exists(os.path.join(tm_data, tm_data_json)):
                        sender.send_message(f"{ColorFormat.AQUA}[{qz}]{ColorFormat.WHITE}你今天已经签到过了哟~")
            return True
        else:
            sender.send_message(f"{ColorFormat.RED}此命令仅玩家可执行!")
            return True

__all__ = ["CatSign"]