import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.6koIKl5M4uGGMPfUL1i6wApc5GaY3sjcEaWZla8QYil5iahhZaoh92aIFPIJCwZBj8PGZFcM1njbIziHZswjqDjcKK7mqRQkW-LnysJVeUy1XSqqEU3kxmV9WHwZeH7VflZs_Nz5Q6fbCkpNahMb4yKoqx9RLQ3kLxkSpW33eCPue98sWFj72cp9OWQNzrNuOLyn9h-qDiUaRGxNkVEquQ"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# 🔹 состояние
fail_streak = 0
doom_active = False


def roll(sides):
    return random.randint(1, sides)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if not event.to_me:
            continue

        text = event.text.lower()

        # 🔹 преимущество
        if text.startswith("/дпре"):
            r1 = roll(20)
            r2 = roll(20)
            result = max(r1, r2)

            if doom_active:
                result -= 2

            response = f"🎲 Преимущество: {r1} и {r2} → {result}"

        # 🔹 помеха
        elif text.startswith("/дпом"):
            r1 = roll(20)
            r2 = roll(20)
            result = min(r1, r2)

            if doom_active:
                result -= 2

            response = f"🎲 Помеха: {r1} и {r2} → {result}"

        # 🔹 /д 20 (ключевая логика)
        elif text.startswith("/д "):
            try:
                sides = int(text.split()[1])
                result = roll(sides)

                # 🔹 Судный час штраф
                if doom_active:
                    result -= 2

                # 🔹 проверка только для d20
                if sides == 20:

                    # крит снимает эффект
                    if result >= 20:
                        fail_streak = 0
                        doom_active = False
                        response = f"🎲 КРИТ! {result} — Судный час рассеялся."
                    
                    elif result < 11:
                        fail_streak += 1

                        # активация
                        if fail_streak > 5:
                            doom_active = True
                            response = (
                                f"💀 Судный час наступил.\n"
                                f"Неудач подряд: {fail_streak}\n"
                                f"Теперь каждый бросок получает -2."
                            )
                        else:
                            response = f"🎲 Выпало: {result} (неудача {fail_streak}/6)"

                    else:
                        fail_streak = 0
                        response = f"🎲 Выпало: {result}"

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

                if doom_active:
                    total -= 2

                response = f"🎲 {count}д{sides}: {rolls} → {total}"

            except:
                response = "Ошибка. Пример: /2д20"

        else:
            continue

        vk.messages.send(
            peer_id=event.peer_id,
            message=response,
            random_id=0
        )
