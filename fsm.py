from transitions import Machine

class MicrowaveOven:
    def __init__(self):
        self.door_closed = True
        self.food_inside = False
        
    def start_heating(self):
        if self.door_closed and self.food_inside:
            print("Дверца закрыта, еда присутствует. Начало нагрева")
            return True
        print("Ошибка запуска: проверьте дверцу и наличие еды!")
        return False
    
    def perform_open_door(self):
        if self.door_closed:
            self.door_closed = False
            print("Дверца открыта")
    
    def perform_close_door(self):
        if not self.door_closed:
            self.door_closed = True
            print("Дверца закрыта")

states = [
    'off',
    'waiting',
    'heating',
    'paused'
]

transitions = [
    # Включение/выключение
    {'trigger': 'power_on', 'source': 'off', 'dest': 'waiting'},
    {'trigger': 'power_off', 'source': '*', 'dest': 'off'},
    
    # Управление нагревом
    {'trigger': 'start', 'source': 'waiting', 'dest': 'heating', 
     'conditions': ['start_heating']},
     
    # Управление дверцей 
    {'trigger': 'open_door', 'source': 'heating', 'dest': 'paused',
     'before': 'perform_open_door'},
    {'trigger': 'open_door', 'source': 'off', 'dest': None,
     'before': 'perform_open_door'},
    {'trigger': 'close_door', 'source': ['paused', 'off'], 
     'dest': None,  
     'before': 'perform_close_door'},
     
    # Таймер
    {'trigger': 'timer_end', 'source': 'heating', 'dest': 'waiting'}
]

oven = MicrowaveOven()
machine = Machine(model=oven, states=states, transitions=transitions, initial='off')

try:
    print(f"1. Начальное состояние: {oven.state}")
    
    oven.power_on()
    print(f"2. После включения: {oven.state}")
    
    oven.food_inside = True
    oven.start()
    print(f"3. После запуска нагрева: {oven.state}")
    
    oven.open_door()
    print(f"4. После открытия дверцы: {oven.state}")
    
    oven.power_off()
    print(f"5. После выключения: {oven.state}")
    
    oven.close_door()
    oven.power_on()
    print(f"6. Повторное включение: {oven.state}")
    
    oven.start()
    print(f"7. Повторный запуск нагрева: {oven.state}")
    
    oven.timer_end()
    print(f"8. После таймера: {oven.state}")
    
    oven.power_off()
    print(f"9. Финальное выключение: {oven.state}")
    
    oven.open_door()
    print(f"10. После открытия: {oven.state}")

except Exception as e:
    print(f"Ошибка: {e}")