from aiogram.dispatcher.filters.state import State, StatesGroup

class NewBillState(StatesGroup):
	select_table = State()
	select_person_quantity = State()
	commit = State()

class Navigation(StatesGroup):
	bill_navigation = State()
	order_navigation = State()