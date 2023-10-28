import logging

from typing import Union
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from ..keyboards.inline.keyboard_orders import create_bills_keyboard, show_order, menu_categories_keyboard
from ..keyboards.callback_factory import bill_callback, menu_callback

from ..misc.states import Navigation

from ..models.dataclasses import Bill, Session, Order

_session = Session()

async def show_bills(message: Union[types.Message, types.CallbackQuery], state: FSMContext,*kwarg):
	await Navigation.bill_navigation.set()

	_session.update()

	async with state.proxy() as storage:
		storage["Session"] =  _session

		_markup = create_bills_keyboard(storage["Session"].get_all_bills(True))

	if isinstance(message, types.Message):
		await message.answer("Rachunki", reply_markup = _markup)

	elif isinstance(message, types.CallbackQuery):
		call = message
		await call.message.edit_text("Rachunki", reply_markup = _markup)
	# await message.answer(f"""Stolik {raw_data["table"]} {raw_data["person"]} osób.""", reply_markup = create_orders_list(raw_data) )


async def open_bill(call: CallbackQuery, state: FSMContext, table):
	await Navigation.bill_navigation.set()

	async with state.proxy() as storage:
		storage["current_table"] = table
		_bill = storage["Session"].get_bill(table)
		_markup = show_order(_bill, table)

	await call.message.edit_text(text = table, reply_markup = _markup)

async def cancel(call: CallbackQuery, state: FSMContext, *kwargs):
	await state.finish()
	await call.message.delete()

async def navigate_orders(call: CallbackQuery, callback_data: dict, state: FSMContext):

	_level = {
		"0":cancel,
		"1":show_bills,
		"2":open_bill,
		"3":open_menu_categories
	}

	_current_level = callback_data.get("level")
	table = callback_data.get("table") if callback_data.get("table") else " "

	_current_function = _level[_current_level]

	await _current_function(call, state, table)



async def open_menu_categories(call: CallbackQuery, state: FSMContext, table):
	await Navigation.order_navigation.set()
	async with state.proxy() as data:
		bill = data["Session"].get_bill(data["current_table"])
		bill.update_orders({"name":"Adrian"})
		logging.log(30, data["Session"].get_bill_orders(data["current_table"]))
	await call.message.edit_text(text = "Menu/Categories",  reply_markup = menu_categories_keyboard(table))

async def navigate_menu(call: CallbackQuery, callback_data: dict, state: FSMContext):
	
	_level = {
		"0":open_bill,
		"1":open_menu_categories
	}

	_current_level = callback_data.get("level")
	_current_function = _level[_current_level]
	table = callback_data.get("table") if callback_data.get("table") else " "

	await _current_function(call, state, table)

def register_orders(dp: Dispatcher):
	dp.register_message_handler(show_bills, Text("Rachunki"))
	# dp.register_callback_query_handler(open_order, order_callback.filter(action = "open_bill"))
	dp.register_callback_query_handler(navigate_orders, bill_callback.filter(action=["open_bill","back","append"]), state = Navigation.bill_navigation)
	dp.register_callback_query_handler(navigate_menu, menu_callback.filter(action=["back"]), state = Navigation.order_navigation)