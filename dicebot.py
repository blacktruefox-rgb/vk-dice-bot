import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.kA2CrMql1-Elz_Kua-6QYwc-qhZ3ly2rM0oa8tD_PSzKTaqu1cCSrjC5OijFIX1pTd-pvKPQnHv25fhMwDpxD7i5EJiPS2VHLaoXOF_fuptUeBc3U6Q7YFQvBXGVngICC6ESgccOZM7kJkCYhUPTG__5vDZ3w4cl4kKd_3pXv-hbdV9qGzBNrLoGIQ9jtHWODPWn5w-k6IwIi75_nkuq9g"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def roll(sides):
    return random.randint(1, sides)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        text = event.text.lower()

        # реагируем только на команды
        if not text.startswith("/"):
            continue

        # 🔹 преимущество
        if text.startswith("/дпре"):
            r1 = roll(20)
            r2 = roll(20)
            response = f"🎲 Преимущество: {r1} и {r2} → {max(r1, r2)}"

        # 🔹 помеха
        elif text.startswith("/дпом"):
            r1 = roll(20)
            r2 = roll(20)
            response = f"🎲 Помеха: {r1} и {r2} → {min(r1, r2)}"

        # 🔹 /д 20
        elif text.startswith("/д "):
            try:
                sides = int(text.split()[1])
                result = roll(sides)

                if result == sides:
                    response = f"🎲 КРИТ! {result} из {sides}"
                elif result == 1:
                    response = f"💀 ПРОВАЛ! {result} из {sides}"
                else:
                    response = f"🎲 Выпало: {result}"

            except:
                response = "Напиши: /д 20"

        # 🔹 /2д20
        elif text.startswith("/") and "д" in text and " " not in text:
            try:
                command = text[1:]
                count, sides = command.split("д")

                count = int(count)
                sides = int(sides)

                rolls = [roll(sides) for _ in range(count)]
                total = sum(rolls)

                response = (
                    f"🎲 {count}д{sides}:\n"
                    f"Броски: {rolls}\n"
                    f"Сумма: {total}"
                )

            except:
                response = "Ошибка. Пример: /2д20"

        else:
            continue

        vk.messages.send(
            peer_id=event.peer_id,
            message=response,
            random_id=0
        )
