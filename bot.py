import vk
import requests
import time
import json
import sys
import os

# ===== НАСТРОЙКИ =====
VK_TOKEN = "vk1.a.UWYdku39Tdr5_CNJJfX8Sa4UiA_7M1vpitIn4Ydpoyszt937fH9RA4L2KqKnPcFX7Ps3Akh_VMNkdDyj1MdUxtpPtvwN7ywT1o0P_45Kg8tLI15hWKeI1eLkEhkGiKyzzG0694o2qOP8wqNGJLkk9eaS2lmbqODbVlyXQGcUm6SBY_Dgaq3rHl5DnhN3yVT_R_P7H3UX4wwOWYcnfbyNpw"
GROUP_ID = 224165070
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzKN2nC90sRigrvKG3G0bUXQWK63hHIgcl-LYVxQ0EvxEL5pUzig_A3r4UqUWd5UpSYDA/exec"
# ===================================

def send_to_table(text):
    try:
        payload = {"text": text}
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("message", "✅ Данные загружены!")
        else:
            return f"❌ Ошибка при отправке в таблицу (код {response.status_code})"
    except Exception as e:
        return f"❌ Ошибка соединения: {e}"

def main():
    vk_session = vk.VK(token=VK_TOKEN)
    longpoll = vk_session.longpoll()
    
    print("🤖 Бот запущен и слушает чат ВК...")
    
    for event in longpoll.listen():
        if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW:
            if event.from_user or event.from_chat:
                msg = event.text.strip()
                user_id = event.user_id
                
                if msg.startswith('#зоркость') or msg.startswith('#лазание'):
                    print(f"📩 Получен отчет: {msg}")
                    response_msg = send_to_table(msg)
                    vk_session.method('messages.send', {
                        'user_id': user_id,
                        'message': response_msg,
                        'random_id': 0
                    })

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Ошибка бота:", e)
