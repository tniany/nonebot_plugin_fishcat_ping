from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.exception import FinishedException
import subprocess
import platform
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__plugin_meta__ = PluginMetadata(
    name="Ping",
    description="通过指令ping检测网络连通性",
    usage="ping [ip/域名]",
    extra={
        "author": "tniay",
        "version": "1.0"
    }
)

# ASCII 艺术：鱼猫
LOGO = r"""
/\___/\    
(  o o  )  FishCat Ping Plugin v1.0
(  =^=  ) 
 (______)  by tniay
"""

# 在插件被加载时显示 LOGO
print(LOGO)

ping = on_command("ping", priority=5, block=True)

@ping.handle()
async def handle_ping(event: MessageEvent):
    logger.debug(f"收到ping命令，完整消息：{event.get_message()}")
    args = str(event.get_message()).strip().split()[1:]
    if not args:
        logger.warning("未提供ping目标")
        await ping.finish("请提供要 ping 的 IP 或域名！")
        return
    
    target = args[0]
    logger.debug(f"准备ping目标：{target}")
    
    # 根据操作系统选择 ping 命令参数
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', target]
    logger.debug(f"执行命令：{command}")
    
    try:
        # 执行 ping 命令
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
        
        logger.debug(f"命令输出：{output}")
        if error:
            logger.error(f"命令错误输出：{error}")
            await ping.finish(f"执行出错：{error}")
            return
            
        # 返回 ping 结果
        await ping.finish(Message(output))
    except FinishedException:
        # 正常结束，不需要记录错误
        raise
    except Exception as e:
        logger.error(f"执行过程中发生异常：{str(e)}", exc_info=True)
        await ping.finish(f"发生错误：{str(e)}") 