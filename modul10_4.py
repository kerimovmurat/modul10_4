import queue
from threading import Thread
import time
from random import randint
from queue import Queue


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest (Thread):
    def __init__(self, name):
        super ().__init__ ()
        self.name = name

    def run(self):
        time.sleep (randint (3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue ()
        self.tables = list (tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            sits = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    guest.start()
                    sits = True
                    break
            if not sits:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any (table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушел(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        print(f'{next_guest.name} вышел(-а) из очереди и сел(-а) за стол номер {table.number}')
                        next_guest.start()


# Создание столов
tables = [Table (number) for number in range (1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest (name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe (*tables)
# Приём гостей
cafe.guest_arrival (*guests)
# Обслуживание гостей
cafe.discuss_guests ()



