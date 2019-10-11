from random import randint

class Item:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __str__(self):
        return "Item: [Value: " + str(self.value) + ", Weight: " + str(self.weight) + "]"


class Backpack:

    def __init__(self, max_weight):
        self.max_weight = max_weight
        self.current_weight = 0
        self.items = []

    def add_item(self, item):
        if item.weight + self.current_weight <= self.max_weight:
            self.items.append(item)
            self.current_weight += item.weight

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight

    def get_total_value(self):
        h = 0
        for i in self.items:
            h += i.value
        return h
    
    def __str__(self):
        string = "["
        for i in self.items:
            if string == "[":
                string = string + i.__str__()
            else:
                string = string + ', ' + i.__str__()
        return string + "]"


class Chromosome:

    def __init__(self, max_weight, mutation_rate=10):
        self.backpack = Backpack(max_weight)
        self.mutation_rate = mutation_rate

    def random_init(self, global_items):
        item = global_items[randint(0, len(global_items)-1)]
        while self.backpack.current_weight + item.weight <= self.backpack.max_weight:
            self.backpack.add_item(item)
            item = global_items[randint(0, len(global_items)-1)]

    def mutate(self, global_items):
        c = randint(1, 100)
        if c <= self.mutation_rate:
            old = randint(0, len(self.backpack.items)-1)
            self.backpack.remove_item(self.backpack.items[old])
            new = randint(0, len(global_items)-1)
            while global_items[new].weight + self.backpack.current_weight < self.backpack.max_weight:
                self.backpack.add_item(global_items[new])
                new = randint(0, len(global_items)-1)

    def get_fitness(self):
        return self.backpack.get_total_value()
    
    def __str__(self):
        return "Chromosome: [Fitness: " + str(self.get_fitness()) + ", Backpack: " + self.backpack.__str__() + "]"


class Population:

    def __init__(self, max_weight, n):
        self.chromosomes = []
        self.items = []
        self.n = n
        self.max_weight = max_weight
        self.generate_items()
        self.generate_pop(max_weight)

    def generate_pop(self, max_weight):
        print("Generating population...")
        for i in range(self.n):
            chromosome = Chromosome(max_weight)
            chromosome.random_init(self.items)
            self.chromosomes.append(chromosome)
            print(chromosome)

    def generate_items(self):
        a = randint(1, 10)
        print("Number of items will be: " + str(a))
        print("Generating items...")
        for i in range(a):
            item = Item(randint(1, a), randint(1, a))
            self.items.append(item)
            print(item)

    def choose_item_from_parent(self, c1, c2):
        parent = randint(1, 2)
        if parent == 1 and c1.get_fitness() != 0:
            item = c1.backpack.items[randint(0, len(c1.backpack.items)-1)]
            c1.backpack.remove_item(item)
        elif c2.get_fitness() != 0:
            item = c2.backpack.items[randint(0, len(c2.backpack.items)-1)]
            c2.backpack.remove_item(item)
        else:
            item = Item(0, 0)
        return item

    def reproduce(self, c1, c2):
        son = Chromosome(self.max_weight)
        item = self.choose_item_from_parent(c1, c2)
        while item.weight + son.backpack.current_weight < son.backpack.max_weight and item.weight != 0:
            son.backpack.add_item(item)
            item = self.choose_item_from_parent(c1, c2)
        son.mutate(self.items)
        print("New son: " + son.__str__())
        return son

    def draw_parent(self):
        a = randint(0, self.get_total_fitness())
        current = 0
        parent = None
        for c in self.chromosomes:
            parent = c
            current += parent.get_fitness()
            if current > a:
                return parent
        return parent

    def get_total_fitness(self):
        total_fitness = 0
        for c in self.chromosomes:
            total_fitness += c.get_fitness()
        return total_fitness

    def select_parents(self):
        self.chromosomes.sort(key=lambda x: x.get_fitness())
        c1 = self.draw_parent()
        c2 = self.draw_parent()
        return c1, c2

    def darwin(self):
        while True:
            new_pop = []
            while len(new_pop) != self.n:
                c1, c2 = self.select_parents()
                new_pop.append(self.reproduce(c1, c2))
            self.chromosomes = new_pop


if __name__ == "__main__":
    max_weight = randint(1, 20)
    n = randint(2, 30)
    print("Max backpack weight is : " + str(max_weight))
    print("Population size will be : " + str(n))
    population = Population(max_weight, n)
    population.darwin()
