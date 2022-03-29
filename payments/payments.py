from vk_api.keyboard import VkKeyboardButton
from vk_api.utils import get_random_id, sjson_dumps

# создание платежных кнопок с определенными действиями и параметрами


class VKPayInterface:
    def __init__(self):
        self.test_user_id = 340953279

    # создать кнопку оплаты 
    def generate_VKpay_keyboard(self, amount=0, user_id=None):
        hash = f"action=pay-to-user&amount={amount}&user_id={user_id}"
        custom_keyboard = sjson_dumps({
        'one_time': False,
        'inline': True,
        'buttons': [[
            {'action': {
                'type': VkKeyboardButton.VKPAY.value,
                'payload': None,
                'hash': hash,
            }}
        ]]})
        return custom_keyboard
    