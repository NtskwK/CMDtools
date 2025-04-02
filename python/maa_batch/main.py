import json
import pathlib
import time

from asst.asst import Asst
from asst.utils import Message, Version, InstanceOptionType
from asst.updater import Updater
from asst.emulator import Bluestacks


check_update = False
# 是否肝活动
campaign = True
money_campain = False
# 服务器选项："Official" | "Bilibili" | "txwy" | "YoStarEN" | "YoStarJP" | "YoStarKR"
servers = ["Bilibili","Official"]
MAA_dir = pathlib.Path('D:\Game\MAA')

@Asst.CallBackType
def my_callback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))

    print(m, d, arg)


# MAA自动化脚本
if __name__ == "__main__":

    # 请设置为存放 dll 文件及资源的路径
    path = MAA_dir

    if check_update:
        print("{}:Check updata".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        # 设置更新器的路径和目标版本并更新
        Updater(path, Version.Nightly).update()
        print("{}:Updata finish!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))

    # 外服需要再额外传入增量资源路径，例如
    # incremental_path=path / 'resource' / 'global' / 'YoStarEN'
    Asst.load(path=path)

    # 若需要获取详细执行信息，请传入 callback 参数
    # 例如 asst = Asst(callback=my_callback)
    asst = Asst()

    # 设置额外配置
    # 触控方案配置
    asst.set_instance_option(InstanceOptionType.touch_type, 'maatouch')
    # 暂停下干员
    # asst.set_instance_option(InstanceOptionType.deployment_with_pause, '1')

    port = 5555
    # 请自行配置 adb 环境变量，或修改为 adb 可执行程序的路径
    while not asst.connect('adb.exe', '127.0.0.1:'+str(port)):
        print('没有检测到可用的连接！正在尝试启动模拟器……')
        port = Bluestacks.get_hyperv_port(r"d:\Game\BlueStacks_nxt\bluestacks.conf", "Pie64") 
        # 启动模拟器。例如启动蓝叠模拟器的多开Pie64，并等待10s
        Bluestacks.launch_emulator_win(r'C:\Program Files\BlueStacks_nxt\HD-Player.exe', 10, "Pie64_1")
        # 获取Hyper-v蓝叠的adb port
               

    print('连接成功')

    # 不同时间，不同战斗计划
    # 获取当前星期
    weekday = time.localtime(time.time()).tm_wday
    # 将星期几转换为字符串表示
    weekday_str = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday]
    print("{}:Link start!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))

    # 龙门币开放日
    money = [2,4,6,7]

    weekday = 1

    if campaign:
        fight_config = {
            # 留空为继续刷上次的关卡
            'stage': '',
            'expiring_medicine': 9,
            'report_to_penguin': True,
            # 'penguin_id': '1234567'
        }
    if weekday == 1:
        fight_config = {
            # 剿灭
            'stage': 'Annihilation',
            'expiring_medicine': 9,
            'report_to_penguin': True,
            # 'penguin_id': '1234567'
        }
    elif weekday in money or money_campain:
        fight_config = {
            'stage': 'CE-6',
            'expiring_medicine': 9,
            'report_to_penguin': True,
            # 'penguin_id': '1234567'
        }
    else:
        fight_config = {
            # 其他时间都去刷经验本
            'stage': 'LS-6',
            'expiring_medicine': 9,
            'report_to_penguin': True,
            # 'penguin_id': '1234567'
        }           

    # 任务轮询
    for select_server in servers:
        # 任务及参数请参考 docs/集成文档.md
        asst.append_task('StartUp',{
            "client_type": select_server,
            "start_game_enabled": True
        })
        asst.append_task('Fight',fight_config)
        asst.append_task('Recruit', {
            'select': [4],
            'confirm': [3, 4],
            'times': 8,
            'expedite':True,
            "expedite_times": 4,
        })
        asst.append_task('Infrast', {
            'facility': [
                "Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"
            ],
            'drones': "Money",
            "threshold": 0.2,
            "dorm_trust_enabled": True
        })
        asst.append_task('Visit')
        asst.append_task('Mall', {
            'shopping': True,
            'buy_first': ['招聘许可', '龙门币'],
            'blacklist': [ '碳'],
        })
        asst.append_task('Award')
        
        # asst.append_task('Copilot', {
        #     'filename': './GA-EX8-raid.json',
        #     'formation': False
        # })

    asst.append_task('Roguelike', {
    "theme": "Sami",
    "mode": 0,
    "investment_enabled": False,
    "stop_when_investment_full": False,
    # "squad": string,        // 开局分队，可选，例如 "突击战术分队" 等，默认 "指挥分队"
    # "roles": string,        // 开局职业组，可选，例如 "先手必胜" 等，默认 "取长补短"
    # "core_char": string,    // 开局干员名，可选，仅支持单个干员中！文！名！。默认识别练度自动选择
    # "use_support": bool,  // 开局干员是否为助战干员，可选，默认 false
    # "use_nonfriend_support": bool,  // 是否可以是非好友助战干员，可选，默认 false，use_support为true时有效
    "refresh_trader_with_dice": True,
})



    asst.start()

    while asst.running():
        time.sleep(0)
    print('任务结束')
    
