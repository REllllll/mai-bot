from nonebot import on_command, on_notice, on_message
from nonebot.params import CommandArg, EventMessage
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot, MessageSegment
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor
from src.libraries.image import *
from PIL import Image


@event_preprocessor
async def preprocessor(bot, event, state):
    if hasattr(event, 'message_type') and event.message_type == "private" and event.sub_type != "friend":
        raise IgnoredException("not reply group temp message")

        
help = on_command('help')


@help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_pic = Image.open('src/pic/help/mai-bot_help.png')
    await help.send(Message([
        MessageSegment("image", {
            "file": f"base64://{str(image_to_base64(help_pic), encoding='utf-8')}"
        })
    ]))


async def _group_poke(bot: Bot, event: Event) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


poke = on_notice(rule=_group_poke, priority=10, block=True)


@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
    await poke.send(Message([
        MessageSegment("poke",  {
           "qq": f"{event.sender_id}"
       })
    ]))


counter = 0
last_message = ''
counter_detector = on_message()

@counter_detector.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    if counter == 0:
        counter += 1
        last_message = str(message)
    elif last_message == str(message):
        counter += 1
        if counter == 3:
            await counter_detector.send(str(message))
    else:
        counter = 0