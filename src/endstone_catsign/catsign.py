import os
import datetime

from endstone import *
from endstone.command import *
from endstone.plugin import Plugin

data_dir = os.path.join(os.getcwd(), "plugins", "CatSign")


class CatSign(Plugin):
    api_version = "0.10"
    authors = ["NewmoonNeko"]

    commands = {
        "qd": {
            "description": "签到指令",
            "usage": ["/qd"],
            "permissions": ["cat.cmd.qd"]
        }
    }

    permissions = {
        "cat.cmd.qd": {
            "description": "签到指令",
            "default": True
        }
    }


    def on_load(self):
        self.logger.info(f"{ColorFormat.AQUA}签到插件加载中...")

    def on_enable(self):
        self.js = self.server.plugin_manager.get_plugin("ye111566_jsonmoney")
        self.um = self.server.plugin_manager.get_plugin("umoney")

        if self.server.plugin_manager.get_plugin("umoney"):
            self.logger.info(f"{ColorFormat.GREEN}检测到UMoney经济插件")
        else:
            self.logger.info(f"{ColorFormat.RED}未检测到UMoney, 插件将卸载")
            self.server.plugin_manager.disable_plugin(self)

        #if you money core is jsonmoney
        """ 
        if self.server.plugin_manager.get_plugin("ye111566_jsonmoney"):
            self.logger.info(f"{ColorFormat.GREEN}检测到jsonmoney经济插件")
        else:
            self.logger.info(f"{ColorFormat.RED}未检测到jsonmoney, 插件将卸载")
            self.server.plugin_manager.disable_plugin(self)
        """

        self.logger.info(f"{ColorFormat.AQUA}CatSign签到插件,\n{ColorFormat.AQUA}作者: NewmoonNeko")

    def on_command(self, sender: CommandSender, cmd: Command, args: list[str]):
        m = 50  # 默认50块
        qz = "签到插件"  # 插件前缀
        u = sender.name
        ny = datetime.datetime.now().year
        nm = datetime.datetime.now().month
        nd = datetime.datetime.now().day
        tm_data = os.path.join(data_dir, f"{ny}-{nm}-{nd}")
        tm_data_json = f"{sender.name}.json"

        #if umoney
        if isinstance(sender, Player):
            match cmd.name:
                case "qd":
                    if not os.path.exists(tm_data):
                        os.mkdir(tm_data)
                        with open(os.path.join(tm_data, tm_data_json), "w") as f:
                            f.write('{"time"}')
                        self.um.api_change_player_money(u, m)
                        #self.js.change(u, m)
                        #if jsonmoney
                        sender.send_message(f"[{qz}]签到成功,你获得了{m}块钱")
                    elif not os.path.exists(tm_data_json):
                        with open(os.path.join(tm_data, tm_data_json), "w") as f:
                            f.write('{"time"}')
                        self.um.api_change_player_money(u, m)
                        #self.js.change(u, m)
                        #if jsonmoney
                        sender.send_message(f"[{qz}]签到成功,你获得了{m}块钱")
                    elif os.path.exists(os.path.join(tm_data, tm_data_json)):
                        sender.send_message(f"[{qz}]你今天已经签到过了哟~")
            return True
        else:
            sender.send_message(f"[{qz}]不要在控制台使用此命令哟")
            return True