# genetic_algorithm.py
import random
from chromosome import Chromosome

class GeneticAlgorithm:
    def __init__(self, pool, depot, crossover_rate=0.7, mutation_rate=0.01,
                 population_size=100, generation_size=1000, elitism=True):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population_size = population_size
        self.generation_size = generation_size
        self.pool = pool
        self.depot = depot
        self.elitism = elitism
        self.current_generation = []
        self.next_generation = []
        self.total_fitness = 0
    
    def solve(self):
        self.create_population()
        self.rank_population()
        
        for i in range(self.generation_size):
            if i % 100 == 0:
                print(f"Generation {i}/{self.generation_size}")
            self.create_next_generation()
            self.rank_population()
        
        return self.current_generation
    
    def create_population(self):
        self.current_generation = [
            Chromosome(self.pool, self.depot, self.mutation_rate)
            for _ in range(self.population_size)
        ]
    
    def rank_population(self):
        self.total_fitness = sum(chromosome.calc_fitness() for chromosome in self.current_generation)
        self.current_generation.sort(key=lambda x: x.fitness)
    
    def create_next_generation(self):
        self.next_generation = []
        if self.elitism:
            self.next_generation.append(self.current_generation[-1])
        
        while len(self.next_generation) < self.population_size:
            parent1 = self.roulette_selection()
            parent2 = self.roulette_selection()
            
            if random.random() < self.crossover_rate:
                child = parent1.crossover(parent2)
            else:
                child = parent1
            
            child.mutate()
            self.next_generation.append(child)
        
        self.current_generation = self.next_generation[:self.population_size]
    
    def roulette_selection(self):
        random_fitness = random.random() * self.total_fitness
        current_fitness = 0
        
        for chromosome in self.current_generation:
            current_fitness += chromosome.fitness
            if current_fitness >= random_fitness:
                return chromosome
        
        return self.current_generation[-1]
