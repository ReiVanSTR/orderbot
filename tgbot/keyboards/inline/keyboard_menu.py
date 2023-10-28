from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from ..callback_factory import table_callback, person_callback, commit_callback

menu_keyboard = InlineKeyboardMarkup(row_width = 2, inline_keyboard = [
	[
		InlineKeyboardButton(text = "Rachunki", callback_data = "1"),
		InlineKeyboardButton(text = "Nowy rachunek", callback_data = "1")
	],
	[
		InlineKeyboardButton(text = "Magazyn", callback_data = "1"),
		InlineKeyboardButton(text = "Zamówienia", callback_data = "1")
	],
	[
		InlineKeyboardButton(text = "...", callback_data = "1"),
		InlineKeyboardButton(text = "Huj huj pizda", callback_data = "1")
	]
])

def create_tables_list(x: int):
	keyboard = []

	cache_row = []
	
	for i in range(1, x):
		_name = f"S{str(i)}"
		if not i%5:
			cache_row.append(InlineKeyboardButton(text = _name, callback_data = table_callback.new("TABLE", _name)))
			keyboard.append(cache_row)
			cache_row = []
		else:
			cache_row.append(InlineKeyboardButton(text = _name, callback_data = table_callback.new("TABLE", _name)))
	keyboard.append(cache_row)

	return InlineKeyboardMarkup(inline_keyboard = keyboard)

def create_person_keyboard():
	keyboard = []

	cache_row = []
	for x in range(1, 16):
		if not x % 3:
			keyboard.append(cache_row)
			cache_row = []
		cache_row.append(InlineKeyboardButton(text = x, callback_data = person_callback.new("PERSON", str(x))))
	
	return InlineKeyboardMarkup(inline_keyboard = keyboard)

def create_commit_keyboard():
	keyboard = [
		[InlineKeyboardButton(text = "Commit", callback_data = commit_callback.new("COMMIT"))],
		[InlineKeyboardButton(text = "Cancel", callback_data = commit_callback.new("CANCEL"))]
	]

	return InlineKeyboardMarkup(inline_keyboard = keyboard)



