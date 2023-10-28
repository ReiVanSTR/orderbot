from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from tgbot.misc.db import get_order
from ..callback_factory import order_callback, bill_callback, cancel_callback, menu_callback

def make_bill_callback_data(level, action="static", table="0"):
	return bill_callback.new(level, action, table)

def make_order_callback_data(action, order_id):
	return order_callback.new(action, order_id)

def create_bills_keyboard(bills_list: list):
	current_level = 1

	keyboard = []

	for bill in bills_list:
		_text = f"""Stolik {bill["table_name"]} {bill["persons"]} osób."""
		_callback_data = make_bill_callback_data(current_level+1, "open_bill", bill["table_name"])
		keyboard.append([InlineKeyboardButton(text = _text, callback_data = _callback_data)])


	keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data(current_level-1, "back"))])
	return InlineKeyboardMarkup(inline_keyboard = keyboard)

def show_order(raw_data: dict, table: str):
	current_level = 2
	keyboard = []

	if raw_data:
		keyboard.append([InlineKeyboardButton(text = "(Nothing)", callback_data = make_bill_callback_data(current_level))])
		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data(current_level-1, "back"))])
		
	else:
		keyboard.append([InlineKeyboardButton(text = "(Nothing)", callback_data = make_bill_callback_data(current_level))])

		cache_row = []

		cache_row.append(InlineKeyboardButton(text = "+", callback_data = make_bill_callback_data(current_level+1,"append", f"{table}")))
		cache_row.append(InlineKeyboardButton(text = "Close", callback_data = make_bill_callback_data(current_level,"close", f"{table}")))
		keyboard.append(cache_row)

		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data(current_level-1, "back"))])


	return InlineKeyboardMarkup(inline_keyboard = keyboard) 

def show_bill(bill):
	current_level = 2
	keyboard = []

	if bill.orders:
		for order in bill.orders:
			_text = f"L{order.order_id} | {order.count_cart()} PLN"


		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data(current_level-1, "back"))])
		
	else:
		keyboard.append([InlineKeyboardButton(text = "(Nothing)", callback_data = make_bill_callback_data(current_level))])

		cache_row = []

		cache_row.append(InlineKeyboardButton(text = "+", callback_data = make_bill_callback_data(current_level+1,"append", f"{table}")))
		cache_row.append(InlineKeyboardButton(text = "Close", callback_data = make_bill_callback_data(current_level,"close", f"{table}")))
		keyboard.append(cache_row)

		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data(current_level-1, "back"))])


	return InlineKeyboardMarkup(inline_keyboard = keyboard) 


def generate_item_keyboard(data: dict):
	pass

def menu_categories_keyboard(table):
	keyboard = []

	keyboard.append([InlineKeyboardButton(text = " << ", callback_data = menu_callback.new("0", "back", table))])

	return InlineKeyboardMarkup(inline_keyboard = keyboard)



