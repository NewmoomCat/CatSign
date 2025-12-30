import json
import os
import time

from endstone import *
from endstone.command import *
from endstone.plugin import Plugin

data_dir = os.path.join(os.getcwd(), "plugins", "CatSign")
config_data_file_path = os.path.join(data_dir, "config.json")

class CatSign(Plugin):
    api_version = "0.10"
    authors = ["NewmoonNeko"]

    commands = {
        "cs": {
            "description": "签到指令",
            "usage": ["/cs"],
            "permissions": ["cat.cmd.cs"]
        }
    }

    permissions = {
        "cat.cmd.cs": {
            "description": "签到指令",
            "default": True
        }
    }

    def __init__(self):
        self.conf_data = {
            "money": 50
        }
        self.money = self.conf_data["money"]

    def on_load(self):
        self.logger.info(f"{ColorFormat.AQUA}签到插件加载中...")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not os.path.exists(config_data_file_path):
            self.logger.info(f"{ColorFormat.RED}未发现配置文件")
            self.logger.info(f"{ColorFormat.YELLOW}创建中...")
            with open(config_data_file_path, "w", encoding="utf-8") as f:
                json_str = json.dumps(self.conf_data, indent=4, ensure_ascii=False)
                f.write(json_str)
            self.conf_data = json.loads(json_str)
            self.logger.info(f"{ColorFormat.GREEN}文件创建成功")


    def on_enable(self):
        with open(config_data_file_path, "r", encoding="utf-8") as f:
            self.conf_data = json.loads(f.read())
        self.um = self.server.plugin_manager.get_plugin("umoney")
        if self.server.plugin_manager.get_plugin("umoney"):
            self.logger.info(f"{ColorFormat.GREEN}检测到UMoney经济插件")
        else:
            self.logger.info(f"{ColorFormat.RED}未检测到UMoney, 插件将卸载")
            self.server.plugin_manager.disable_plugin(self)
        self.logger.info(f"{ColorFormat.AQUA}CatSign签到插件,\n{ColorFormat.AQUA}作者: NewmoonNeko")

    def on_command(self, sender: CommandSender, cmd: Command, args: list[str]):
        m = self.money
        u = sender.name
        if cmd.name == "cs":
            if isinstance(sender, Player):
                self.um.api_get_money_data()
                self.um.api_change_player_money(u, m)
                sender.send_message(f"{ColorFormat.GREEN}签到成功, 获得{m}块钱!")
            elif isinstance(sender, Player):
                sender.send_message(f"{ColorFormat.YELLOW}你今天签到过了, 不要重复签到")
            else:
                sender.send_message(f"{ColorFormat.YELLOW}不要在控制台使用此命令哟!")
            return True
        return False