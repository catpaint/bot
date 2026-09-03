import os
import aiohttp
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8893590777:AAG4Icx7IVi57fY6aQLvCtoWR6xaH_Xzab0"
HEADERS = {"User-Agent": "WEAO-3PService"}
BASE_URL = "https://weao.xyz/api"
CACHE_FILE = "exploits_cache.json"
SUBS_FILE = "subscribers.json"

bot = Bot(token=TOKEN)
dp = Dispatcher()

USER_LANG = {}

def load_subscribers():
    if os.path.exists(SUBS_FILE):
        try:
            with open(SUBS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_subscribers(subs):
    try:
        with open(SUBS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(subs), f, ensure_ascii=False, indent=2)
    except Exception:
        pass

SUBSCRIBERS = load_subscribers()

TEXTS = {
    "ru": {
        "menu_title": "🛠 <b>Главное меню:</b>",
        "all_exploits": "⚡ Все эксплойты",
        "free_exploits": "🆓 Бесплатные",
        "undetected_exploits": "🛡 Не детекты",
        "roblox_versions": "📊 Версии Roblox",
        "select_exploit": "🎯 <b>Список ({count} шт):</b>",
        "not_found": "❌ Не найдено",
        "api_error": "❌ Ошибка запроса к АПИ",
        "back": "⬅️ Назад",
        "lang_set": "✅ Язык установлен!",
        "versions_title": "📱 <b>Тип версий Roblox:</b>",
        "current_ver": "🔴 Текущие (Live)",
        "future_ver": "🟡 Будущие (Future)",
        "past_ver": "📜 Прошлые (Past)",
        "sub_on": "🔔 Включить уведомления",
        "sub_off": "🔕 Выключить уведомления",
        "sub_done": "🔔 Уведомления включены!",
        "unsub_done": "🔕 Уведомления выключены!",
        "notify_updated": "🔔 <b>Эксплойт обновился!</b>\n\n👑 <b>{title}</b> [{platform}]\n🏷 Версия: {version}\n🔄 Статус: 🟢 Обновлен\n📅 Дата: {date}",
        "version": "версия",
        "updated": "обновлен",
        "status": "статус",
        "detected": "детект",
        "platform": "платформа",
        "type": "тип",
        "free": "бесплатный",
        "cost": "цена",
        "keysystem": "система ключей",
        "decompiler": "декомпилятор",
        "multiInject": "мульти-инжект",
        "raknet": "поддержка raknet",
        "clientmods": "обход модов клиента",
        "uncStatus": "unc статус",
        "uncPct": "unc %",
        "suncPct": "sunc %",
        "rbxVer": "rbx version",
        "website": "сайт",
        "discord": "дискорд",
        "purchase": "покупка",
        "yes": "да",
        "no": "нет",
        "updated_str": "обновлен",
        "not_updated_str": "не обновлен"
    },
    "en": {
        "menu_title": "🛠 <b>Main Menu:</b>",
        "all_exploits": "⚡ All Exploits",
        "free_exploits": "🆓 Free",
        "undetected_exploits": "🛡 Undetected",
        "roblox_versions": "📊 Roblox Versions",
        "select_exploit": "🎯 <b>List ({count} pcs):</b>",
        "not_found": "❌ Not found",
        "api_error": "❌ API Request Error",
        "back": "⬅️ Back",
        "lang_set": "✅ Language set!",
        "versions_title": "📱 <b>Roblox Version Types:</b>",
        "current_ver": "🔴 Current (Live)",
        "future_ver": "🟡 Future",
        "past_ver": "📜 Past",
        "sub_on": "🔔 Enable notifications",
        "sub_off": "🔕 Disable notifications",
        "sub_done": "🔔 Notifications enabled!",
        "unsub_done": "🔕 Notifications disabled!",
        "notify_updated": "🔔 <b>Exploit Updated!</b>\n\n👑 <b>{title}</b> [{platform}]\n🏷 Version: {version}\n🔄 Status: 🟢 Updated\n📅 Date: {date}",
        "version": "version",
        "updated": "updated",
        "status": "status",
        "detected": "detected",
        "platform": "platform",
        "type": "type",
        "free": "free",
        "cost": "price",
        "keysystem": "key system",
        "decompiler": "decompiler",
        "multiInject": "multi-inject",
        "raknet": "raknet support",
        "clientmods": "client mods bypass",
        "uncStatus": "unc status",
        "uncPct": "unc %",
        "suncPct": "sunc %",
        "rbxVer": "rbx version",
        "website": "website",
        "discord": "discord",
        "purchase": "purchase",
        "yes": "yes",
        "no": "no",
        "updated_str": "updated",
        "not_updated_str": "not updated"
    }
}

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json()
            return None

def get_txt(user_id, key):
    lang = USER_LANG.get(user_id, "ru")
    return TEXTS[lang].get(key, key)

def get_main_kb(user_id):
    sub_text = get_txt(user_id, "sub_off") if user_id in SUBSCRIBERS else get_txt(user_id, "sub_on")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_txt(user_id, "all_exploits"), callback_data="exploits_all")],
        [InlineKeyboardButton(text="🪟 Windows", callback_data="filter_Windows"), InlineKeyboardButton(text="🤖 Android", callback_data="filter_Android")],
        [InlineKeyboardButton(text="🍏 Mac", callback_data="filter_Mac"), InlineKeyboardButton(text="📱 iOS", callback_data="filter_iOS")],
        [InlineKeyboardButton(text=get_txt(user_id, "free_exploits"), callback_data="filter_Free"), InlineKeyboardButton(text=get_txt(user_id, "undetected_exploits"), callback_data="filter_Undetected")],
        [InlineKeyboardButton(text=get_txt(user_id, "roblox_versions"), callback_data="versions_menu")],
        [InlineKeyboardButton(text=sub_text, callback_data="toggle_sub")],
        [InlineKeyboardButton(text="🌐 Language / Язык", callback_data="ask_lang")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="setlang_en")]
    ])
    await message.answer("🌐 <b>Choose language / Выберите язык:</b>", parse_mode="HTML", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("setlang_"))
async def process_set_lang(callback: CallbackQuery):
    lang = callback.data.split("setlang_")[1]
    USER_LANG[callback.from_user.id] = lang
    await callback.message.edit_text(get_txt(callback.from_user.id, "menu_title"), parse_mode="HTML", reply_markup=get_main_kb(callback.from_user.id))

@dp.callback_query(lambda c: c.data == "ask_lang")
async def process_ask_lang(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="setlang_en")]
    ])
    await callback.message.edit_text("🌐 <b>Choose language / Выберите язык:</b>", parse_mode="HTML", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "toggle_sub")
async def process_toggle_sub(callback: CallbackQuery):
    uid = callback.from_user.id
    if uid in SUBSCRIBERS:
        SUBSCRIBERS.remove(uid)
        save_subscribers(SUBSCRIBERS)
        await callback.answer(get_txt(uid, "unsub_done"))
    else:
        SUBSCRIBERS.add(uid)
        save_subscribers(SUBSCRIBERS)
        await callback.answer(get_txt(uid, "sub_done"))
    await callback.message.edit_text(get_txt(uid, "menu_title"), parse_mode="HTML", reply_markup=get_main_kb(uid))

@dp.callback_query(lambda c: c.data.startswith("exploits_") or c.data.startswith("filter_"))
async def process_exploits_list(callback: CallbackQuery):
    uid = callback.from_user.id
    data = await fetch_json(f"{BASE_URL}/status/exploits")
    if not data:
        await callback.message.edit_text(get_txt(uid, "api_error"))
        return
    
    seen = set()
    unique_items = []
    for item in data:
        key = (item.get("title"), item.get("platform"))
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
            
    filter_type = callback.data.replace("exploits_", "").replace("filter_", "")
    
    filtered = []
    for item in unique_items:
        if filter_type == "all":
            filtered.append(item)
        elif filter_type == "Free" and item.get("free"):
            filtered.append(item)
        elif filter_type == "Undetected" and not item.get("detected"):
            filtered.append(item)
        elif item.get("platform") == filter_type:
            filtered.append(item)
            
    kb = []
    for item in filtered:
        title = item.get("title", "Unknown")
        platform = item.get("platform", "")
        status_icon = "🟢" if item.get("updateStatus") else "🔴"
        cb_id = item.get("_id") or title
        kb.append([InlineKeyboardButton(text=f"{status_icon} {title} [{platform}]", callback_data=f"exp_{cb_id}")])
        
    kb.append([InlineKeyboardButton(text=get_txt(uid, "back"), callback_data="main")])
    await callback.message.edit_text(get_txt(uid, "select_exploit").format(count=len(filtered)), parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(lambda c: c.data.startswith("exp_"))
async def process_exploit_info(callback: CallbackQuery):
    uid = callback.from_user.id
    target_id = callback.data.split("exp_")[1]
    all_data = await fetch_json(f"{BASE_URL}/status/exploits")
    data = None
    if all_data:
        for item in all_data:
            if item.get("_id") == target_id or item.get("title") == target_id:
                data = item
                break
                
    if not data:
        await callback.message.edit_text(get_txt(uid, "not_found"))
        return
        
    yes_str = get_txt(uid, "yes")
    no_str = get_txt(uid, "no")
    upd_str = get_txt(uid, "updated_str")
    not_upd_str = get_txt(uid, "not_updated_str")

    text = (
        f"👑 <b>{data.get('title')}</b>\n\n"
        f"🏷 <b>{get_txt(uid, 'version')}:</b> {data.get('version')}\n"
        f"📅 <b>{get_txt(uid, 'updated')}:</b> {data.get('updatedDate')}\n"
        f"🔄 <b>{get_txt(uid, 'status')}:</b> {'🟢 ' + upd_str if data.get('updateStatus') else '🔴 ' + not_upd_str}\n"
        f"🛡 <b>{get_txt(uid, 'detected')}:</b> {'⚠️ ' + yes_str if data.get('detected') else '✅ ' + no_str}\n"
        f"💻 <b>{get_txt(uid, 'platform')}:</b> {data.get('platform')}\n"
        f"⚙️ <b>{get_txt(uid, 'type')}:</b> {data.get('extype')}\n"
        f"💰 <b>{get_txt(uid, 'free')}:</b> {'✅ ' + yes_str if data.get('free') else '❌ ' + no_str}\n"
        f"💵 <b>{get_txt(uid, 'cost')}:</b> {data.get('cost', 'N/A')}\n"
        f"🔑 <b>{get_txt(uid, 'keysystem')}:</b> {'🔑 ' + yes_str if data.get('keysystem') else '❌ ' + no_str}\n"
        f"📜 <b>{get_txt(uid, 'decompiler')}:</b> {'✅ ' + yes_str if data.get('decompiler') else '❌ ' + no_str}\n"
        f"🔀 <b>{get_txt(uid, 'multiInject')}:</b> {'✅ ' + yes_str if data.get('multiInject') else '❌ ' + no_str}\n"
        f"🌐 <b>{get_txt(uid, 'raknet')}:</b> {'✅ ' + yes_str if data.get('raknet') else '❌ ' + no_str}\n"
        f"🪟 <b>{get_txt(uid, 'clientmods')}:</b> {'✅ ' + yes_str if data.get('clientmods') else '❌ ' + no_str}\n"
        f"📊 <b>{get_txt(uid, 'uncStatus')}:</b> {'✅ ' + yes_str if data.get('uncStatus') else '❌ ' + no_str}\n"
        f"📈 <b>{get_txt(uid, 'uncPct')}:</b> {data.get('uncPercentage', 0)}%\n"
        f"📊 <b>{get_txt(uid, 'suncPct')}:</b> {data.get('suncPercentage', 0)}%\n"
        f"🎮 <b>{get_txt(uid, 'rbxVer')}:</b> <code>{data.get('rbxversion')}</code>\n\n"
        f"🌐 <b>{get_txt(uid, 'website')}:</b> {data.get('websitelink', 'N/A')}\n"
        f"💬 <b>{get_txt(uid, 'discord')}:</b> {data.get('discordlink', 'N/A')}\n"
        f"🛒 <b>{get_txt(uid, 'purchase')}:</b> {data.get('purchaselink', 'N/A')}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=get_txt(uid, "back"), callback_data="exploits_all")]])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("versions_"))
async def process_versions_menu(callback: CallbackQuery):
    uid = callback.from_user.id
    v_type = callback.data.replace("versions_", "")
    if v_type == "menu":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_txt(uid, "current_ver"), callback_data="versions_current")],
            [InlineKeyboardButton(text=get_txt(uid, "future_ver"), callback_data="versions_future")],
            [InlineKeyboardButton(text=get_txt(uid, "past_ver"), callback_data="versions_past")],
            [InlineKeyboardButton(text=get_txt(uid, "back"), callback_data="main")]
        ])
        await callback.message.edit_text(get_txt(uid, "versions_title"), parse_mode="HTML", reply_markup=kb)
        return

    data = await fetch_json(f"{BASE_URL}/versions/{v_type}")
    if not data:
        await callback.message.edit_text(get_txt(uid, "api_error"))
        return
        
    text = f"🚀 <b>Roblox ({v_type}):</b>\n\n"
    if "Windows" in data:
        text += f"🪟 <b>windows:</b> <code>{data.get('Windows')}</code>\n🕒 <i>{data.get('WindowsDate')}</i>\n\n"
    if "Mac" in data:
        text += f"🍎 <b>mac:</b> <code>{data.get('Mac')}</code>\n🕒 <i>{data.get('MacDate')}</i>\n\n"
    if "Android" in data:
        text += f"🤖 <b>android:</b> <code>{data.get('Android')}</code>\n🕒 <i>{data.get('AndroidDate')}</i>\n\n"
    if "iOS" in data:
        text += f"📱 <b>ios:</b> <code>{data.get('iOS')}</code>\n🕒 <i>{data.get('iOSDate')}</i>"
        
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=get_txt(uid, "back"), callback_data="versions_menu")]])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "main")
async def process_main(callback: CallbackQuery):
    uid = callback.from_user.id
    await callback.message.edit_text(get_txt(uid, "menu_title"), parse_mode="HTML", reply_markup=get_main_kb(uid))

async def check_updates_loop():
    while True:
        try:
            await asyncio.sleep(2)
            data = await fetch_json(f"{BASE_URL}/status/exploits")
            if not data:
                continue
                
            old_cache = {}
            if os.path.exists(CACHE_FILE):
                try:
                    with open(CACHE_FILE, "r", encoding="utf-8") as f:
                        old_cache = json.load(f)
                except Exception:
                    pass
                    
            new_cache = {}
            for item in data:
                key = f"{item.get('title')}_{item.get('platform')}"
                upd = item.get("updateStatus")
                ver = item.get("version")
                new_cache[key] = {"updateStatus": upd, "version": ver}
                
                if key in old_cache:
                    old_upd = old_cache[key].get("updateStatus")
                    old_ver = old_cache[key].get("version")
                    if (not old_upd and upd) or (old_ver != ver and upd):
                        for user_id in list(SUBSCRIBERS):
                            msg = get_txt(user_id, "notify_updated").format(
                                title=item.get("title"),
                                platform=item.get("platform"),
                                version=ver,
                                date=item.get("updatedDate")
                            )
                            try:
                                await bot.send_message(user_id, msg, parse_mode="HTML")
                            except Exception:
                                pass
                                
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(new_cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

async def main():
    asyncio.create_task(check_updates_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
