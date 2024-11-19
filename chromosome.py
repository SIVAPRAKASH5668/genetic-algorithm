# chromosome.py
import random
import math
from location import Location

class Chromosome:
    def __init__(self, pool=None, depot=None, mutation_rate=0, genes=None):
        self.pool = pool or []
        self.depot = depot
        self.genes = genes or []
        self.length = len(genes) if genes else len(pool)
        self.mutation_rate = mutation_rate
        self.fitness = 0
        if not genes:
            self.create_genes()
    
    def create_genes(self):
        self.genes = [self.depot]
        available_locations = self.pool.copy()
        while available_locations:
            location = random.choice(available_locations)
            available_locations.remove(location)
            self.genes.append(location)
        self.genes.append(self.depot)
        self.length = len(self.genes)
    
    def calc_fitness(self):
        total_distance = 0
        for i in range(1, self.length):
            distance = math.sqrt(
                (self.genes[i-1].x - self.genes[i].x) ** 2 +
                (self.genes[i-1].y - self.genes[i].y) ** 2
            )
            total_distance += distance
        self.fitness = 1 / total_distance if total_distance > 0 else 0
        return self.fitness
    
    def crossover(self, chromosome):
        pos = random.randint(1, self.length - 2)
        offspring_genes = (
            self.genes[1:pos] +
            [g for g in chromosome.genes[pos:-1] if g not in self.genes[1:pos]] +
            [g for g in self.genes[pos:-1] if g not in chromosome.genes[pos:-1]] +
            [g for g in chromosome.genes[1:pos] if g not in self.genes[1:pos]]
        )
        offspring = Chromosome(None, self.depot, self.mutation_rate, 
                              [self.depot] + offspring_genes + [self.depot])
        return offspring
    
    def mutate(self):
        for i in range(1, self.length - 1):
            if random.random() < self.mutation_rate:
                j = random.randint(1, self.length - 2)
                self.genes[i], self.genes[j] = self.genes[j], self.genes[i]
        return self
