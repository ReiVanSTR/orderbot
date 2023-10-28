from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

static_keyboard = ReplyKeyboardMarkup(keyboard = [
	[
		KeyboardButton(text = "Nowy rachunek")

	],
	[
		KeyboardButton(text = "Rachunki"),
		KeyboardButton(text = "Historia sprzedaży")
	],
	[
		KeyboardButton(text = "Huj"),
		KeyboardButton(text = "Pizda")
	],
], resize_keyboard=True)