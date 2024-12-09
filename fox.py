# леша даже не думай нахуй, яйца оторву

from playwright.sync_api import sync_playwright
from time import sleep

VERSION = '0.1'
 
base_url = 'https://app.atommobility.com/sharing/vehicles'
user_agent = 'Mozilla/5.0 (Macintosh; ARM64 Mac OS X 14_7_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'
local_storage_key = 'atom-frontend-K31QYJD6HKetiB5FF0Tb4bFNcPhlUfu18m2x9SIS8MaMim9I0tXEfwnz9XU9ahYWEpQsmXmGfUSVp3IWo+oZJA'
local_storage_value = '{"accessToken":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTczMzk1MzQ0MCwiaWF0IjoxNzMzNjk0MjQwLCJ0eXAiOiJKV1QifQ.eyJpZCI6NDE2N30.o2ChWsXmZkgObJCsr0beiZk6UOI4s8PnfLBeM6UjxPw","expiresIn":259200,"flow":"SHARING"}'

def send_command(code: str, command: str, input_value: int = 0, count: int = 2):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()
        page.goto("about:blank")
        page.add_init_script(f"""
            localStorage.setItem('{local_storage_key}', '{local_storage_value}');
        """)
    
        page.goto(base_url)

        try:
            # Ожидание поля ввода
            input_selector = "input#mat-input-1"
            page.wait_for_selector(input_selector, timeout=5000)
            input_field = page.locator(input_selector)
            input_field.fill(code)
            
            # Поиск строки с нужным кодом
            scooter_selector = f"tr.mat-row:has(td.cdk-column-vehicle_number:text('{code}'))"
            page.wait_for_selector(scooter_selector, timeout=5000)
            scooter = page.locator(scooter_selector)
            scooter.click()

            # Открытие панели команд
            nav_cmd_btn_selector = "span:text(' Commands ')"
            page.wait_for_selector(nav_cmd_btn_selector, timeout=5000)
            nav_cmd_btn = page.locator(nav_cmd_btn_selector)
            nav_cmd_btn.click()

            # Поиск команды
            cmd_selector = f"tr:has(td.cdk-column-command:has-text('{command}'))"
            page.wait_for_selector(cmd_selector, timeout=5000)
            cmd = page.locator(cmd_selector)
            cmd.click()

            # Выполнение команды
            if input_value == 0:
                button = cmd.locator('button.mat-icon-button')
                for i in range(count):
                    button.click()
                    sleep(0.09)
            else:
                input_field = cmd.locator('input')
                input_field.fill(str(input_value))
                sleep(0.1)
                button = cmd.locator('button.mat-icon-button')
                for i in range(count):
                    button.click()
                    sleep(0.09)

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            page.close()
            browser.close()
            
COMMANDS = {
    "UNLOCK": 0,
    "LOCK": 1,
    "UNLOCK_ENCHANTED": 2,
    "UNLOCK_MECHANICAL_LOCK": 3,
    "LOCK_MECHANICAL_LOCK": 4,
    "REBOOT": 5,
    "POWER_OFF": 6,
    "UPDATE_GEO_INFO": 7,
    "WARN": 8,
    "HEADLIGHT_ON": 9,
    "HEADLIGHT_OFF": 10,
    "REARLIGHT_ON": 11,
    "REARLIGHT_ON_FORCED": 12,
    "REARLIGHT_OFF": 13,
    "ENGINE_ON": 14,
    "ENGINE_OFF": 15,
    "WIRELESS_CHARGING_ON": 16,
    "WIRELESS_CHARGING_OFF": 17,
    "SET_DISPLAY_UNIT_YD": 18,
    "SET_DISPLAY_UNIT_KM": 19,
    "MODE_NORMAL": 20,
    "MODE_SPORT": 21,
    "MAX_SPEED_LIMIT_FROM_0_TO_63_KM/H": 22,
    "SET_ALARM_INTERVAL_FROM_5_TO_3600_SECONDS": 23,
    "SET_VIBRATION_ALARM_INTERVAL_FROM_0_TO_300_SECONDS": 24,
    "SET_NEVER_TURN_OFF_GPS": 25,
    "SET_TURN_OFF_GPS_WHEN_NOT_NEEDED": 26,
    "AGPS_MODE_ON": 27,
    "AGPS_MODE_OFF": 28,
    "BACKUP_VOICE_PLAY_ENABLED": 29,
    "BACKUP_VOICE_PLAY_DISABLED": 30,
    "VOICE_PLAY_ENABLED": 31,
    "VOICE_PLAY_DISABLED": 32,
    "POWER_OFF_ENABLED": 33,
    "POWER_OFF_DISABLED": 34,
    "SET_VOLUME_FROM_0_TO_7": 35,
    "SET_ALARM_VOLUME_FROM_0_TO_7": 36,
    "GREEN_LED_ENABLED": 37,
    "GREEN_LED_DISABLED": 38,
    "LED_MODE_CONSTANT": 39,
    "LED_MODE_FLASHES": 40,
    "LED_BLINK_FREQUENCY_FROM_20_TO_100": 41,
    "MECHANICAL_LOCK_ENABLED": 42,
    "MECHANICAL_LOCK_DISABLED": 43,
    "ELECTRONIC_BELL_ENABLED": 44,
    "ELECTRONIC_BELL_DISABLED": 45,
    "NFC_WORK_MODE_ENABLED": 46,
    "NFC_WORK_MODE_DISABLED": 47,
    "SCOOTER_BATTERY_HEATING_ON": 48,
    "SCOOTER_BATTERY_HEATING_OFF": 49,
    "SET_MECHANICAL_LOCK_TYPE_BATTERY_LOCK_A": 50,
    "SET_MECHANICAL_LOCK_TYPE_BATTERY_LOCK_B": 51,
    "SET_MECHANICAL_LOCK_TYPE_PILE_LOCK": 52,
    "SET_MECHANICAL_LOCK_TYPE_BASKET_LOCK": 53,
    "SET_MOVE_DETECTION_NON_MOVEMENT_DURATION_FROM_1_TO_255": 54,
    "SET_MOVE_DETECTION_MOVEMENT_DURATION_FROM_1_TO_50": 55,
    "SET_MOVE_DETECTION_SENSITIVITY_FROM_2_TO_19": 56,
    "SET_VEHICLE_IN_NORMAL_MODE": 57,
    "SET_VEHICLE_IN_TEST_MODE": 58,
    "SET_5_SEC_REPORT_INTERVAL": 59,
    "SET_DEFAULT_REPORT_INTERVAL": 60,
    "SET_ALARM_REPORT_INTERVAL": 61,
    "REQUEST_CONFIGURATION": 62,
    "REQUEST_VER_CONFIGURATION": 63,
    "REQUEST_CANVER_CONFIGURATION": 64,
    "ENABLE_BLE_UNLOCK": 65,
    "DISABLE_BLE_UNLOCK": 66,
    "UPDATE_BLE_BROADCAST_NAME": 67,
    "ENABLE_NFC_WORK_MODE": 68,
    "DISABLE_NFC_WORK_MODE": 69,
    "UPDATE_CUSTOMER_ID": 70,
    "SET_BATTERY_LOCK_ALARM_TIMES": 71,
    "SET_NFC_TAG_ID": 72,
    "SET_BLE_PASSWORD": 73,
    "START_UPDATE_FIRMWARE": 74,
    "START_UPDATE_BATTERY_FIRMWARE": 75,
    "START_UPDATE_BATTERY_LOCK_FIRMWARE": 76,
    "STOP_UPDATE_FIRMWARE": 77,
    "START_UPDATE_RING_AUDIO_FILE": 78,
    "CONFIGURE_HELMET_BOX_SELECTION_1": 79,
    "START_UPDATE_LOCK_AUDIO": 80,
    "START_UPDATE_UNLOCK_AUDIO": 81,
    "CONFIGURE_HELMET_BOX_SELECTION_2": 82,
    "START_UPDATE_ALARM_AUDIO": 83,
    "UNLOCK_HELMET_BOX": 84
}

COMMANDS_RU = {
    "разблокировать": 'UNLOCK',
    "разблокировать самокат": "UNLOCK",
    "анлок": "UNLOCK",
    "унлок": "UNLOCK",
    "анлокнуть": "UNLOCK",
    "заблокировать": "LOCK",
    "заблокировать самокат": "LOCK",
    "лок": "LOCK",
    "локнуть": "LOCK",
    "анлок энчанчед": "UNLOCK_ENCHANTED",
    "унлок энчанчед": "UNLOCK_ENCHANTED",
    "пиздато разблокировть": "UNLOCK_ENCHANTED",
    "замок": "UNLOCK_MECHANICAL_LOCK",
    "открыть замок": "UNLOCK_MECHANICAL_LOCK",
    "открыть деку": "UNLOCK_MECHANICAL_LOCK",
    "открой деку": "UNLOCK_MECHANICAL_LOCK",
    "открой дека": "UNLOCK_MECHANICAL_LOCK",
    "открыть самокат": "UNLOCK_MECHANICAL_LOCK",
    "разблокировать замок": "UNLOCK_MECHANICAL_LOCK",
    "анлок механикал лок": "UNLOCK_MECHANICAL_LOCK",
    "унлок механикал лок": "UNLOCK_MECHANICAL_LOCK",
    "перезагрузка": "REBOOT",
    "рестарт": "REBOOT",
    "перезапуск": "REBOOT",
    "ребут": "REBOOT",
    "выключить": "POWER_OFF",
    "выключить самокат": "POWER_OFF",
    "павер офф": "POWER_OFF",
    "повер офф": "POWER_OFF",
    "вырубить": "POWER_OFF",
    "вырубить нахуй": "POWER_OFF",
    "обновить геолокацию": "UPDATE_GEO_INFO",
    "обновить гео": "UPDATE_GEO_INFO",
    "апдейт гео инфо": "UPDATE_GEO_INFO",
    "геолокация": "UPDATE_GEO_INFO",
    "найти самокат": "WARN",
    "варн": "WARN",
    "сигнал": "WARN",
    "включить передние фары": "HEADLIGHT_ON",
    "передние фары": "HEADLIGHT_ON",
    "хеадлайт он": "HEADLIGHT_ON",
    "передний свет": "HEADLIGHT_ON",
    "включить передний свет": "HEADLIGHT_ON",
    "отключить передние фары": "HEADLIGHT_OFF",
    "выключить передние фары": "HEADLIGHT_OFF",
    "хеадлайт офф": "HEADLIGHT_OFF",
    "выключить передний свет": "HEADLIGHT_OFF",
    "отключить передний свет": "HEADLIGHT_OFF",
    "включить задние фары": "REARLIGHT_ON",
    "задние фары": "REARLIGHT_ON",
    "реарлайт он": "REARLIGHT_ON",
    "задний свет": "REARLIGHT_ON",
    "включить задний свет": "REARLIGHT_ON",
    "включить принудительные задние фары": "REARLIGHT_ON_FORCED",
    "принудительные задние фары": "REARLIGHT_ON_FORCED",
    "реарлайт он форсед": "REARLIGHT_ON_FORCED",
    "принудительный задний свет": "REARLIGHT_ON_FORCED",
    "включить принудительный задний свет": "REARLIGHT_ON_FORCED",
    "отключить задние фары": "REARLIGHT_OFF",
    "выключить задние фары": "REARLIGHT_OFF",
    "реарлайт офф": "REARLIGHT_OFF",
    "выключить задний свет": "REARLIGHT_OFF",
    "отключить задний свет": "REARLIGHT_OFF",
    "беспроводная зарядка": "WIRELESS_CHARGING_ON",
    "включить беспроводную зарядку": "WIRELESS_CHARGING_ON",
    "вайрлесс чарджинг он": "WIRELESS_CHARGING_ON",
    "выключить беспроводную зарядку": "WIRELESS_CHARGING_OFF",
    "отключить беспроводную зарядку": "WIRELESS_CHARGING_OFF",
    "вайрлесс чарджинг офф": "WIRELESS_CHARGING_OFF",
    "включить километры": "SET_DISPLAY_UNIT_KM",
    "километры": "SET_DISPLAY_UNIT_KM",
    "показывать кмч": "SET_DISPLAY_UNIT_KM",
    "показывать км/ч": "SET_DISPLAY_UNIT_KM",
    "сет дисплей юнит км": "SET_DISPLAY_UNIT_KM",
    "обычный режим": "MODE_NORMAL",
    "дефолтный режим": "MODE_NORMAL",
    "выключить спорт режим": "MODE_NORMAL",
    "моде нормал": "MODE_NORMAL",
    "дефолт": "MODE_NORMAL",
    "спорт режим": "MODE_SPORT",
    "турбо режим": "MODE_SPORT",
    "включить спорт режим": "MODE_SPORT",
    "включить турбо режим": "MODE_SPORT",
    "обновить замок": "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "обновить драйвера на замок": "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "обновить дрова на замок": "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "перепрошить замок": "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "прошить замок": "START_UPDATE_BATTERY_LOCK_FIRMWARE",
    "обновить прошивку замка": "START_UPDATE_BATTERY_LOCK_FIRMWARE"
}