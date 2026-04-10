import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.6koIKl5M4uGGMPfUL1i6wApc5GaY3sjcEaWZla8QYil5iahhZaoh92aIFPIJCwZBj8PGZFcM1njbIziHZswjqDjcKK7mqRQkW-LnysJVeUy1XSqqEU3kxmV9WHwZeH7VflZs_Nz5Q6fbCkpNahMb4yKoqx9RLQ3kLxkSpW33eCPue98sWFj72cp9OWQNzrNuOLyn9h-qDiUaRGxNkVEquQ"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def roll(sides):
    return random.randint(1, sides)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        # 🔹 реагируем только на команды (избегаем спама)
        if not event.to_me:
            continue

        text = event.text.lower()

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
                    response = f"🎲 Выпало: {result} (1-{sides})"

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
