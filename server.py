import os
import json
import logging
import exceptions
from obshak import Obshak
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

# GROUP_ID = os.getenv("VK_GROUP_ID")
# GROUP_TOKEN = os.getenv("VK_GROUP_TOKEN")
from payments.payments import VKPayInterface

logging.basicConfig(level=logging.INFO)
GROUP_ID = '211937698'
GROUP_TOKEN = 'd71c0693eee4737b603bd4424ebd21b0cbd2280fcb5855b0cff5e62ca031dde1171d2563e727359a022ce'
API_VERSION = "5.131"

CALLBACK_TYPES = ("show_snackbar", "open_link", "open_app")

vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
long_poll = VkBotLongPoll(vk_session, GROUP_ID)

keyboard_default = VkKeyboard(one_time=False, inline=True)
keyboard_help = VkKeyboard(one_time=False, inline=True)
keyboard_menu = VkKeyboard(one_time=False)
payments = VKPayInterface()
obshak = Obshak()


def send_message(peer_id, keyboard=None, message=''):
    vk.messages.send(
        peer_id=peer_id,
        random_id=get_random_id(),
        keyboard=keyboard,
        message=message
    )


def confirm_keyboard(test_data, i):
    keyboard_1 = VkKeyboard(one_time=False, inline=True)
    keyboard_1.add_callback_button(
        label='Подтвердить',
        color=VkKeyboardColor.SECONDARY,
        payload={"type": 'show_snackbar-' + str(test_data.people[i]) + '-' + str(test_data.creditor),
                 'text': str(test_data.amount[i]) + ' ' + str(test_data.generate_message(i))
                 }
    )
    return keyboard_1.get_keyboard()


def confirm(event):
    obshak.add_debtor(event.object.payload.get('type').split('-')[1],
                      event.object.payload.get('type').split('-')[2],
                      event.object.payload.get('text').split(' ')[0],
                      event.object.payload.get('text').split(' ')[1])
    event.object.payload['type'] = str(event.object.payload['type']).split('-')[0]
    vk.messages.sendMessageEventAnswer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=json.dumps(event.object.payload),
    )
    vk.messages.edit(
        peer_id=event.obj.peer_id,
        message=event.object.payload['text'],
        conversation_message_id=event.obj.conversation_message_id,
    )


def reject(event):
    vk.messages.sendMessageEventAnswer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=json.dumps({
            'type': 'show_snackbar',
            'text': 'Вы не можете подтвердить задолженность за другого человека'
        }),
    )

def resolve_name(id: str):
    return vk_session.method("users.get", {"user_ids": id})

def show_credits(user_id, peer_id):
    creditors = obshak.get_creditors(user_id)
    print(creditors)
    if not creditors:
        send_message(peer_id, message='Вы никому не должны')
    for i in creditors:
        keyboard_pay = payments.generate_VKpay_keyboard(i[0], i[2])
        user_id = str(i[1])
        user_screen_name = resolve_name(str(i[1]))
        amount = str(i[2]) 
        send_message(peer_id, keyboard_pay,
                     'Пользователь: ' + user_screen_name + 'сумма:' + amount + '\n' + i[4] + '\n' + i[3])


def show_debtors(user_id, peer_id):
    debtors = obshak.get_debtors(user_id)
    if not debtors:
        send_message(peer_id, message='Вам никто не должен')
    for i in debtors:
        user_screen_name = resolve_name(str(i[1]))
        send_message(peer_id, message='Пользователь: ' + user_screen_name + ' сумма: ' + str(i[2]) + '\n' + i[4] + '\n' + i[3])


def start_long_polling():
    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            """Обработка текстовых сообщений"""
            print("New message to bot: " + event.message.text)
            try:
                if event.message.text.__str__().find('Показать долги') != -1\
                        or event.message.text.__str__().find('@club211937698 Показать долги') != -1:
                    show_credits(event.message.from_id, event.message.peer_id)
                elif event.message.text.__str__().find('Показать должников') != -1\
                        or event.message.text.__str__().find('@club211937698 Показать должников') != -1:
                    show_debtors(event.message.from_id, event.message.peer_id)
                else:
                    test_data = obshak.process_message(event.message.text.__str__(), event.message.from_id)
                    for j in range(len(test_data.people)):
                        test_data.people[j] = resolve_name(test_data.people[j])
                    for i in range(len(test_data.people)):
                        send_message(event.message.peer_id, confirm_keyboard(test_data, i), test_data.generate_message(i))
            except exceptions.NotCorrectMessage as e:
                send_message(event.message.peer_id, keyboard_menu.get_keyboard(), 'Я вас не понял')
                send_message(event.message.peer_id, keyboard_help.get_keyboard(), 'Что именно вы хотели?')
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            """Обработка всех клавиатур"""
            if event.object.payload.get('type').split('-')[0] in CALLBACK_TYPES:
                if str(event.object.user_id) == str(event.object.payload.get('type').split('-')[1]):
                    confirm(event)
                else:
                    reject(event)
            elif event.object.payload.get('type') == 'keyboard-help':
                vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=event.object.payload['text'],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=keyboard_default.get_keyboard(),
                )
            elif event.object.payload.get('type') == 'show_credits':
                show_credits(event.obj.user_id, event.obj.peer_id)
                vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=event.object.payload['text'],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=keyboard_default.get_keyboard(),
                )
            elif event.object.payload.get('type') == 'show_debtors':
                show_debtors(event.obj.user_id, event.obj.peer_id)
                vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=event.object.payload['text'],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=keyboard_default.get_keyboard(),
                )


def default_keyboard():
    keyboard_default.add_callback_button(
        label='Показать долги',
        color=VkKeyboardColor.PRIMARY,
        payload={"type": 'show_credits',
                 'text': 'Что именно вы хотели?'}
    )
    keyboard_default.add_line()
    keyboard_default.add_callback_button(
        label='Показать должников',
        color=VkKeyboardColor.PRIMARY,
        payload={"type": 'show_debtors',
                 'text': 'Что именно вы хотели?'}
    )
    return keyboard_default.get_keyboard()


def help_keyboard():
    keyboard_help.add_callback_button(
        label='Помощь',
        color=VkKeyboardColor.PRIMARY,
        payload={"type": 'keyboard-help',
                 'text': 'Что именно вы хотели?'}
    )
    return keyboard_help.get_keyboard()


def menu_keyboard():
    keyboard_menu.add_button('Показать долги', color=VkKeyboardColor.POSITIVE)
    keyboard_menu.add_line()
    keyboard_menu.add_button('Показать должников', color=VkKeyboardColor.POSITIVE)

# obshak.add_testdata_db()


if __name__ == '__main__':
    default_keyboard()
    help_keyboard()
    menu_keyboard()
    start_long_polling()
