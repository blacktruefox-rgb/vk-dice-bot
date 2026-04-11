import vk_api
import random
import time
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.6koIKl5M4uGGMPfUL1i6wApc5GaY3sjcEaWZla8QYil5iahhZaoh92aIFPIJCwZBj8PGZFcM1njbIziHZswjqDjcKK7mqRQkW-LnysJVeUy1XSqqEU3kxmV9WHwZeH7VflZs_Nz5Q6fbCkpNahMb4yKoqx9RLQ3kLxkSpW33eCPue98sWFj72cp9OWQNzrNuOLyn9h-qDiUaRGxNkVEquQ"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def roll(sides):
    return random.randint(1, sides)


# 🔹 cooldown
last_used = {}
COOLDOWN = 86400


# 🔹 предсказания (сокращённый список, но ты можешь вставить весь)
predictions = [
"Твоя дорога откроется там, где ты перестанешь искать.",
"Неожиданная встреча изменит твой взгляд на прошлое.",
"Тишина принесёт больше ответов, чем слова.",
"Малое усилие приведёт к большому результату.",
"Потеря окажется началом приобретения.",
"Вода укажет направление, если ты не будешь сопротивляться.",
"Чужая ошибка станет твоим шансом.",
"Старое знание пригодится в новом деле.",
"Ожидание будет дольше, чем ты рассчитываешь.",
"Тот, кого ты недооценил, окажется важным."
]


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        try:
            text = event.text.lower()

            if not text.startswith("/"):
                continue

            user_id = event.from_id
            now = int(time.time())

            # 🔹 /предсказание
            if text.startswith("/предсказание"):

                if user_id in last_used:
                    diff = now - last_used[user_id]

                    if diff < COOLDOWN:
                        hours_left = int((COOLDOWN - diff) / 3600) + 1
                        response = f"⏳ Уже использовано. Попробуй через {hours_left} ч."
                    else:
                        last_used[user_id] = now
                        response = random.choice(predictions)
                else:
                    last_used[user_id] = now
                    response = random.choice(predictions)

            # 🔹 преимущество
            elif text.startswith("/дпре"):
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
                    parts = command.split("д")

                    if len(parts) != 2:
                        raise ValueError

                    count = int(parts[0])
                    sides = int(parts[1])

                    rolls = [roll(sides) for _ in range(count)]
                    total = sum(rolls)

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

        except Exception as e:
            print("ERROR:", e)
