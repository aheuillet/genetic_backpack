from random import randint
import copy  

class Item:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __str__(self):
        return "Item: [Value: " + str(self.value) + ", Weight: " + str(self.weight) + "]"
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value and self.weight == other.weight
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.value != other.value or self.weight != other.weight
        return True


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

    def __init__(self, max_weight, global_items, mutation_rate=5):
        self.backpack = Backpack(max_weight)
        self.mutation_rate = mutation_rate
        self.available_items = global_items.copy() # Creating a copy of global items array to preserve it

    def random_init(self):
        item = self.available_items[randint(0, len(self.available_items)-1)]
        while (self.backpack.current_weight + item.weight <= self.backpack.max_weight) or (self.get_fitness() == 0):
            self.backpack.add_item(item)
            self.available_items.remove(item)
            if len(self.available_items) != 0:
                item = self.available_items[randint(0, len(self.available_items)-1)]
            else:
                break

    def mutate(self):
        c = randint(1, 100)
        if c <= self.mutation_rate:
            old = self.backpack.items[randint(0, len(self.backpack.items)-1)]
            self.available_items.append(old)
            self.backpack.remove_item(old)
            new = self.available_items[randint(0, len(self.available_items)-1)]
            while new.weight + self.backpack.current_weight > self.backpack.max_weight:
                new = self.available_items[randint(0, len(self.available_items)-1)]
            self.backpack.add_item(new)
            self.available_items.remove(new)

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
            chromosome = Chromosome(max_weight, self.items)
            chromosome.random_init()
            self.chromosomes.append(chromosome)
            print(chromosome)

    def generate_items(self):
        a = randint(2, self.max_weight)
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
        son = Chromosome(self.max_weight, self.items)
        item = self.choose_item_from_parent(c1, c2)
        while item.weight + son.backpack.current_weight <= son.backpack.max_weight and item.weight != 0:
            if item in son.available_items:
                son.backpack.add_item(item)
                son.available_items.remove(item)
            item = self.choose_item_from_parent(c1, c2)
        son.mutate()
        assert son.get_fitness() != 0
        return son

    def draw_parent(self):
        a = randint(0, self.get_total_fitness())
        current = 0
        parent = None
        for c in self.chromosomes:
            parent = c
            current += parent.get_fitness()
            if current > a:
                self.chromosomes.remove(parent)
                return parent
        return parent

    def get_total_fitness(self):
        total_fitness = 0
        for c in self.chromosomes:
            total_fitness += c.get_fitness()
        return total_fitness

    def select_parents(self):
        parents = []
        self.chromosomes.sort(key=lambda x: x.get_fitness())
        for i in range(int(self.n/2)):
            parents.append(self.draw_parent())
        parents.sort(key=lambda x: x.get_fitness())
        return parents
    
    def check_completion(self, generation_iteration):
        self.chromosomes.sort(key=lambda x: x.get_fitness())
        if self.chromosomes[len(self.chromosomes) - 1].get_fitness() == self.chromosomes[0].get_fitness() and generation_iteration >= 10:
            return True
        return False

    def darwin(self, max_generations=1000, gui=None):
        print("Breeding population...")
        current_gen = 0
        while current_gen != max_generations and not(self.check_completion(current_gen)):
            parents = self.select_parents()
            new_pop = []
            while len(new_pop) + len(parents) != self.n:
                c1 = parents[randint(0, len(parents) - 1)]
                c2 = parents[randint(0, len(parents) - 1)]
                new_pop.append(self.reproduce(copy.deepcopy(c1), copy.deepcopy(c2)))
            new_pop.extend(parents)
            self.chromosomes = new_pop
            current_gen += 1
            if gui is not None:
               if gui.OneLineProgressMeter('Darwin', current_gen+1, max_generations, 'key','Breeding population...') == False:
                   break
        print("DONE")
    
    def print_results(self):
        print("====RESULTS====")
        strong, weak = self.get_results()
        print("Strongest child: " + str(strong))
        print("Weakest child: " + str(weak))
    
    def get_results(self):
        self.chromosomes.sort(key=lambda x: x.get_fitness())
        return self.chromosomes.pop(), self.chromosomes[0]


if __name__ == "__main__":
    seed = randint(20, 100)
    max_weight = int(seed/2)
    n = int(0.75 * seed)
    print("Max backpack weight is : " + str(max_weight))
    print("Population size will be : " + str(n))
    population = Population(max_weight, n)
    population.darwin()
    population.get_results()
