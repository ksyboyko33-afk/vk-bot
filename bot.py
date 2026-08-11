import vk
import requests
import time
import json
import sys
import re

# ===== НАСТРОЙКИ =====
VK_TOKEN = "vk1.a.UWYdku39Tdr5_CNJJfX8Sa4UiA_7M1vpitIn4Ydpoyszt937fH9RA4L2KqKnPcFX7Ps3Akh_VMNkdDyj1MdUxtpPtvwN7ywT1o0P_45Kg8tLI15hWKeI1eLkEhkGiKyzzG0694o2qOP8wqNGJLkk9eaS2lmbqODbVlyXQGcUm6SBY_Dgaq3rHl5DnhN3yVT_R_P7H3UX4wwOWYcnfbyNpw"
GROUP_ID = 224165070
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzKN2nC90sRigrvKG3G0bUXQWK63hHIgcl-LYVxQ0EvxEL5pUzig_A3r4UqUWd5UpSYDA/exec"
# ===================================

def send_to_table(text, reply_to=None):
    try:
        payload = {"text": text, "reply_to": reply_to}
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("message", "✅ Данные загружены!")
        else:
            return f"❌ Ошибка при отправке в таблицу (код {response.status_code})"
    except Exception as e:
        return f"❌ Ошибка соединения: {e}"

def main():
    # Инициализация через API (новая версия библиотеки vk)
    vk_session = vk.API(token=VK_TOKEN, version='5.131')
    longpoll = vk_session.longpoll()
    
    print("🤖 Бот запущен и слушает чат ВК...")
    
    for event in longpoll.listen():
        if event.type == vk.longpoll.EventType.MESSAGE_NEW:
            msg = event.text.strip()
            user_id = event.from_id
            
            # Игнорируем сообщения с тегами помощи
            if msg.startswith('#помощь_лазание') or msg.startswith('#помощь_зоркость'):
                continue

            # Обработка отмены (если есть ответ на сообщение)
            reply_to = None
            if event.message.get('reply_message'):
                reply_to = event.message['reply_message']['text']

            # Если сообщение начинается с хэштега
            if msg.startswith('#вступил') or msg.startswith('#лазание') or msg.startswith('#зоркость') or msg.startswith('#урок') or msg.startswith('#отмена'):
                print(f"📩 Получен отчет: {msg}")
                response_msg = send_to_table(msg, reply_to)
                
                # Отправляем ответ
                vk_session.messages.send(
                    user_id=user_id, 
                    message=response_msg, 
                    random_id=int(time.time())
                )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Ошибка бота:", e)
