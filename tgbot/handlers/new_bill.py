import logging

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from ..keyboards.callback_factory import table_callback, person_callback, commit_callback
from ..keyboards.inline.keyboard_menu import create_tables_list, create_person_keyboard, create_commit_keyboard
from ..misc.states import NewBillState
from ..misc.db import rc, set_new_bill
from ..misc.other import real_time

async def start(message: types.Message):
	await NewBillState.select_table.set()
	await message.answer("Wybierz stolik", reply_markup = create_tables_list(11))

async def process_select_table(call: CallbackQuery, callback_data: dict, state: FSMContext):
	await NewBillState.select_person_quantity.set()

	async with state.proxy() as data:
			data["table"] = callback_data["name"]
			logging.log(30, callback_data)

	await call.message.edit_text("Ile osob?", reply_markup = create_person_keyboard())

async def process_select_person(call: CallbackQuery, callback_data: dict, state: FSMContext):
	await NewBillState.commit.set()


	async with state.proxy() as data:
			data["person"] = callback_data["quantity"]
			data["amount"] = 0
			_text = f"""
					Zgadza się?
				Stolik {data["table"]}
				Dla {data["person"]} osób
				"""
	await call.message.edit_text(_text, reply_markup = create_commit_keyboard())

async def process_commit(call: CallbackQuery, callback_data: dict, state: FSMContext):
	if callback_data['action'] == "COMMIT":
		async with state.proxy() as data:
			order = {
		      "table_name":data["table"],
		      "persons":int(data["person"]),
		      "orders":[],
		      "time": real_time()
		    }
			set_new_bill(order)
		await call.message.edit_text("Rachunek został zrobiony", reply_markup = None)
	else:
		await call.message.edit_reply_markup(reply_markup = None)
		await call.message.delete()
	await state.finish()

# async def start2(message: types.Message):
# 	await NewBillState.bill_name.set()

# 	await message.answer("Wybierz stolik")

def register_new_bill(dp: Dispatcher):
	dp.register_message_handler(start, Text("Nowy rachunek"))
	# dp.register_message_handler(start2, Text("Huj"))
	dp.register_callback_query_handler(process_select_table, table_callback.filter(action = "TABLE"), state = NewBillState.select_table)
	dp.register_callback_query_handler(process_select_person, person_callback.filter(action = "PERSON"), state = NewBillState.select_person_quantity)
	dp.register_callback_query_handler(process_commit, commit_callback.filter(action = ["COMMIT","CANCEL"]), state = NewBillState.commit)