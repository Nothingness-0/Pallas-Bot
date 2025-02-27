from nonebot import on_command , on_message
from nonebot.adapters.cqhttp import MessageSegment, Message, permission, GroupMessageEvent
from nonebot.rule import keyword, startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from tools.pixiv.pixiv import a60

status = {}

can = on_message(rule=startswith('牛牛涩涩'),
                priority=10,
                permission=permission.GROUP)

@can.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    s = status.get(event.group_id)
    if s:
        can.block = True
        p = await a60()
        url = f'https://www.pixiv.net/artworks/{p.id}'
        msg: Message = MessageSegment.text(url) + MessageSegment.image(file=p.pic)
        await can.finish(msg)
    else:
        can.block = False

cannot = on_message(rule=startswith('牛牛涩涩'),
                  priority=17,
                  permission=permission.GROUP)


@cannot.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    s = status.get(event.group_id)
    if not s:
        cannot.block = True
        await cannot.finish("听啊，悲鸣停止了。这是幸福的和平到来前的宁静。")
    else:
        cannot.block = False

status = {}

switch = on_message(
    rule=keyword("牛牛可以涩涩", "牛牛不可以涩涩"), 
    block=True,
    priority=5,
    permission=permission.GROUP_ADMIN | permission.GROUP_OWNER)

@switch.handle()
async def sw(bot: Bot, event: GroupMessageEvent, state: T_State):
    s = event.get_plaintext()
    if '不' in s:
        status[event.group_id] = False
        await switch.finish("再转身回头的时候，我们将带着胜利归来。")
    else:
        status[event.group_id] = True
        await switch.finish("不需畏惧，我们会战胜那些鲁莽的家伙！")
