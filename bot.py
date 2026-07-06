import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")  # We will set this in Render

MENU = {
    "fries": {"name": "Medium Fries", "price": 6.00},
    "meat":  {"name": "Meat (200g)", "price": 5.00},
    "salad": {"name": "Salad", "price": 3.00},
    "drink": {"name": "Soft Drink", "price": 3.00},
}

cart = {}

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"🌙 Welcome to **Purcy All Night Grill**!\n\n"
        "Tap the buttons below to order.",
        reply_markup=get_main_menu()
    )

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 View Menu", callback_data="show_menu")],
        [InlineKeyboardButton(text="🛒 View Cart", callback_data="show_cart")],
        [InlineKeyboardButton(text="✅ Place Order", callback_data="place_order")]
    ])

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "show_menu":
        kb = []
        for key, item in MENU.items():
            kb.append([InlineKeyboardButton(
                text=f"{item['name']} — XCG {item['price']:.2f}",
                callback_data=f"add_{key}"
            )])
        kb.append([InlineKeyboardButton(text="← Back", callback_data="back_main")])
        await callback.message.edit_text("**Menu**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    elif callback.data.startswith("add_"):
        item_key = callback.data[4:]
        user_id = callback.from_user.id
        if user_id not in cart:
            cart[user_id] = []
        cart[user_id].append(MENU[item_key])
        await callback.answer(f"✅ Added {MENU[item_key]['name']}")

    elif callback.data == "show_cart":
        user_id = callback.from_user.id
        if not cart.get(user_id):
            await callback.answer("Cart is empty!")
            return
        items = cart[user_id]
        total = sum(item["price"] for item in items)
        text = "🛒 Your Cart:\n\n" + "\n".join([f"• {i['name']}" for i in items]) + f"\n\nTotal: XCG {total:.2f}"
        await callback.message.edit_text(text)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
