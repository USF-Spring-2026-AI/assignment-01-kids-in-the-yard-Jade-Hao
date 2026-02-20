import pandas as pd
import numpy as np
import math
from collections import Counter


class Person:
    def __init__(self, first_name, last_name, birth_year, life_span):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.death_year = birth_year + life_span
        self.children = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class PersonFactory:
    """Uses Pandas for high-level data manipulation."""
    def __init__(self):
        # Initializing DataFrames
        self.df_life = None
        self.df_rates = None
        self.df_last_names = None

    def load_data(self):
        """Loading data using Pandas instead of standard csv module."""
        self.df_life = pd.read_csv('life_expectancy.csv')
        self.df_rates = pd.read_csv('birth_and_marriage_rates.csv').set_index('decade')
        
        # Merging last names with their probabilities via a Join/Merge operation
        df_names_raw = pd.read_csv('last_names.csv')
        df_probs = pd.read_csv('rank_to_probability.csv')
        self.df_last_names = pd.merge(df_names_raw, df_probs, on='rank')

    def get_life_span(self, birth_year):
        """Using .iloc and conditional filtering to find expectancy."""
        decade = (birth_year // 10) * 10
        # Complex filtering: Find the row where decade matches, then access expectancy
        try:
            # Using .iloc[0] to grab the first matching scalar value
            base_expectancy = self.df_life.loc[self.df_life['decade'] == decade, 'expectancy'].iloc[0]
        except IndexError:
            base_expectancy = 75.0
            
        return base_expectancy + np.random.uniform(-10, 10)

    def get_random_surname(self):
        """Weighted selection using Pandas/Numpy."""
        # Selection based on the probability column
        name = np.random.choice(
            self.df_last_names['name'], 
            p=self.df_last_names['probability'] / self.df_last_names['probability'].sum()
        )
        return name

class FamilyTree:
    def __init__(self, factory):
        self.factory = factory
        self.people = []

    def generate(self):
        """Simulation logic with vectorized child count calculation."""
        # Initial ancestors
        p1 = Person("Founder1", "Smith", 1950, self.factory.get_life_span(1950))
        p2 = Person("Founder2", "Jones", 1950, self.factory.get_life_span(1950))
        self.people.extend([p1, p2])

        idx = 0
        while idx < len(self.people):
            parent = self.people[idx]
            idx += 1

            if parent.birth_year > 2075: continue

            # Accessing rates via Pandas Index
            decade = (parent.birth_year // 10) * 10
            if decade in self.factory.df_rates.index:
                # Using .at for fast scalar access
                birth_rate = self.factory.df_rates.at[decade, 'birth_rate']
                
                # Formula: ceil(rate +/- 1.5)
                num_kids = math.ceil(birth_rate + np.random.uniform(-1.5, 1.5))
                num_kids = max(0, num_kids)

                for _ in range(num_kids):
                    b_year = np.random.randint(parent.birth_year + 25, parent.birth_year + 45)
                    if b_year > 2120: continue
                    
                    child = Person("Name", parent.last_name, b_year, self.factory.get_life_span(b_year))
                    parent.children.append(child)
                    self.people.append(child)

    def report(self):
        df = pd.DataFrame([{
            'name': p.full_name, 
            'birth': p.birth_year, 
            'decade': (p.birth_year // 10) * 10
        } for p in self.people])

        print(f"Total Population: {len(df)}")
        print("\nDecade Breakdown:")
        print(df['decade'].value_counts().sort_index())
        
        print("\nDuplicate Names:")
        print(df[df.duplicated('name')]['name'].unique())

if __name__ == "__main__":
    fac = PersonFactory()
    fac.load_data()
    tree = FamilyTree(fac)
    tree.generate()
    tree.report()