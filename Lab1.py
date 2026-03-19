class Humanity:
    def __init__(self, population, avg_age, tech_level):
        self._population = population
        self._avg_age = avg_age
        self._tech_level = tech_level

    # --- Інкапсуляція ---
    def get_population(self):
        return self._population

    def set_population(self, value):
        if value > 0:
            self._population = value
        else:
            print("Помилка: населення не може бути від'ємним")

    # --- Метод ---
    def show_info(self):
        print("=== Людство ===")
        print(f"Населення: {self._population}")
        print(f"Середній вік: {self._avg_age}")
        print(f"Рівень технологій: {self._tech_level}")


# --- Дочірній клас ---
class Country(Humanity):
    def __init__(self, population, avg_age, tech_level, name):
        super().__init__(population, avg_age, tech_level)
        self.name = name

    # --- Поліморфізм ---
    def show_info(self):
        print(f"=== Країна: {self.name} ===")
        print(f"Населення: {self._population}")
        print(f"Середній вік: {self._avg_age}")
        print(f"Рівень технологій: {self._tech_level}")

    def grow_population(self, amount):
        self._population += amount
        print(f"Населення збільшилось на {amount}")


# --- ТЕСТ ПРОГРАМИ ---
h = Humanity(8000000000, 30, 5)
c = Country(40000000, 35, 4, "Україна")

h.show_info()
print()

c.show_info()
c.grow_population(100000)
c.set_population(41000000)
c.show_info()