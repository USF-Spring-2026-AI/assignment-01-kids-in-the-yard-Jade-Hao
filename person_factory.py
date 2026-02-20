from person import Person
import pandas as pd 
import random

"""
Responsible for reading data files and generating Person instances.
"""

class PersonFactory:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.life_expectancy = None
        self.birth_marriage_rates = None

    def reading_files(self):                                    #Load required files + prepare weighted last-name list
        self.first_name = pd.read_csv("first_names.csv")        #Reading files help: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html#
        self.last_names = pd.read_csv("last_names.csv")
        self.life_expectancy = pd.read_csv("life_expectancy.csv")
        self.rank_probabilities = (
            pd.read_csv("rank_to_probability.csv", header=None)
            .squeeze()                                          #Help: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.squeeze.html
            .tolist()
         ) 
        self.birth_marriage_rates = pd.read_csv("birth_and_marriage_rates.csv")

        self.last_name_list = []                                #Weighted lists for random last name selection
        self.last_name_weight = []

        ranks = list(self.last_names["Rank"])                   #Help:https://www.w3schools.com/python/ref_func_list.asp
        last_names = list(self.last_names["LastName"])

        for i in range(len(ranks)):
            rank = ranks[i]
            last_name = last_names[i]
            probability = self.rank_probabilities[rank - 1]     #Rank is 1-indexed, list index is 0-based
            self.last_name_list.append(last_name)
            self.last_name_weight.append(probability)

    """
    Generate a person born in a given give year 
    + converts birth year to a decade string
    """
    def generate_person(self, year_born):
        decade_year = f"{(year_born // 10) * 10}s"              #Convert birth year to decade string

        names_in_decade = self.first_name[self.first_name["decade"] == decade_year] #Filter first name by decade
        if names_in_decade.empty:
            names_in_decade = self.first_name[self.first_name["decade"] == "2010s"] #Fall back to 2010 data if decade not avaliable (Suggestion from ChatGPT)
        names = list(names_in_decade["name"])
        frequency = list(names_in_decade["frequency"])

        name_list = random.choices(names, weights = frequency, k = 1)
        first_name = name_list[0]

        last_name = random.choices(self.last_name_list, weights = self.last_name_weight, k = 1)[0] #Help: https://www.w3schools.com/python/ref_random_choices.asp
        gender = random.choice(["M", "F"])                      #Random gender assignment

        death_year = self.generate_year_died(year_born)         #Estimate year of death using life expectancy data

        return Person(first_name, last_name, gender, year_born, death_year)
        
    def generate_year_died(self, year_born):
        decade_year = (year_born // 10) * 10
        
        row = self.life_expectancy[self.life_expectancy["Year"] == decade_year]

        if not row.empty:
            expected_life = int(row["Period life expectancy at birth"].values[0])
        else:
            expected_life = 75                                  #Fallback if value is missing (Suggestion from ChatGPT)
        
        return year_born + random.randint(expected_life - 10, expected_life + 10)               #Add ±10 years for randomness 
    
    def make_partner(self, person):
        if person.partner is not None:                          #No remarriage 
            return None
        
        decade_year = f"{(person.year_of_birth //10) * 10}s"

        row = self.birth_marriage_rates[self.birth_marriage_rates["decade"] == decade_year]
    
        if row.empty:
            return None
    
        marriage_rate = row["marriage_rate"].values[0]
    
        if random.random() < marriage_rate:                     #Probability-based marriage decision
            partner_birth_year = person.year_of_birth + random.randint(-10, 10)
            if partner_birth_year < 1950:
                partner_birth_year = 1950
            partner = self.generate_person(partner_birth_year)

            while partner.last_name == person.last_name:        #Avoid same last name
                partner = self.generate_person(partner_birth_year)

            person.set_partner(partner)                         #Assign partnership both ways
            partner.set_partner(person)

            return partner
        return None

    def create_children(self, person, founder_names):           #Generate children based on birth rate
        decade_year = f"{(person.year_of_birth //10) * 10}s"
        
        row = self.birth_marriage_rates[self.birth_marriage_rates["decade"]== decade_year]
        if row.empty:
            return []
        
        expected_birth_rate = row["birth_rate"].values[0]

        min_births = expected_birth_rate - 1.5                  #Compute min and max children
        max_births = expected_birth_rate + 1.5

        min_children = int(min_births)                          #Round bounds to whole numbers
        if min_births > min_children:
            min_children += 1

        # Round max_births down
        max_children = int(max_births)
        if max_births > max_children:
            max_children += 1

        min_children = max(0, min_children)
        max_children = max(min_children, max_children)

        number_of_keiki = random.randint(min_children, max_children)

        children = []

        start = person.year_of_birth + 25                       #Can have children = 25-45
        end = person.year_of_birth + 45
        if start > 2120:
            return []
        end = min(end, 2120)
        if start > end:
            return []

        child_break = (end - start) / number_of_keiki if number_of_keiki > 0 else 0 #Help: https://www.geeksforgeeks.org/python/ternary-operator-in-python/ 

        for i in range(number_of_keiki):
            child_born = int(start + i * child_break)
            child = self.generate_person(child_born)
            child.last_name = random.choice(founder_names)         #Get names from founder/elders
            person.add_child(child)
            children.append(child)

        return children