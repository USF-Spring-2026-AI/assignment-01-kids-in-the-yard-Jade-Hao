from person_factory import PersonFactory
import pandas as pd 

"""
Control generation and analysis of the family tree
"""
class FamilyTree:
    def __init__(self):
        self.person_factory = PersonFactory()
        self.people = []

    def generate_family(self): 
        print("Reading files.... ")   
        print("Generating family tree...")                              #Generate the initial elders + expand the family tree

        self.person_factory.reading_files()
        parent1 =self.person_factory.generate_person(1950)              #Create two people born in 1950
        parent2 = self.person_factory.generate_person(1950)
      
        self.founder_names = [                                          #Set orginal last names 
            parent1.last_name, 
            parent2.last_name
        ]
        parent1.set_partner(parent2)                                    #Establish relationship
        parent2.set_partner(parent1)

        self.people.extend([parent1, parent2])
        self.expand_family_tree(parent1, self.founder_names)            #Recursively expand children
        self.expand_family_tree(parent2, self.founder_names)

    def expand_family_tree (self, person, founder_names):
        if person.year_of_birth > 2120:
            return                                                      #Base case: STOP IF BEYOND SIMULATION TIME FRAME
        
        partner = person.partner
        if person.partner is None:                                      #Make sure that the person has a partner if eligible
            partner = self.person_factory.make_partner(person)
            if partner:
                self.people.append(partner)
        
        children = []
        if person.partner is None:
            children = self.person_factory.create_children(person, founder_names) 
        elif person.year_of_birth <= person.partner.year_of_birth:
            children = self.person_factory.create_children(person, founder_names)

        for child in children:
            if child not in self.people:
                self.people.append(child)
            self.expand_family_tree(child, founder_names)               #Recursively expand next generation



    def number_of_family_members(self):                                 #Return total number of people in the tree
        return len(self.people)
    
    def people_by_year_of_birth(self):  
        people_by_year = {}
        for person in self.people:
           decade = (person.year_of_birth // 10) * 10

           if decade in people_by_year:
               people_by_year[decade] += 1
           else:
                people_by_year[decade] = 1

        sorted_count = {}
        for decade in sorted(people_by_year):
            sorted_count[decade] = people_by_year[decade]
        return sorted_count                                             #Return sorted list by decade
    
    def duplicate_names(self):                                          #Return FULL names that appear more than once
        name_count = {}
        for person in self.people:
            name = person.get_full_name()
            if name in name_count:
                name_count[name] += 1
            else:
                name_count[name] = 1
        duplicates = [name for name in name_count if name_count[name] > 1]
        return duplicates
    
    def run_program(self):                                                 #Run with same look as PDF
        while True:
            print("\nAre you interested in: ")
            print("(T)otal number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("(Q)uit")

            user_choice = input("> ").strip().upper()

            if user_choice == "T":
                print(f"The tree contains: {self.number_of_family_members()} people total")
            elif user_choice == "D":
                outcome = self.people_by_year_of_birth()
                for decade in outcome:
                    print(f"{decade}: {outcome[decade]}")
            elif user_choice == "N":
                duplicates = self.duplicate_names()
                if duplicates:
                    duplicates.sort()                                       #Alphabetical Order
                    print(f"There are {len(duplicates)} duplicate names in the tree:")
                    for name in duplicates:
                        print(f"* {name}")
                else:
                    print("No duplicate names found.")
            elif user_choice == "Q":
                break
            else:
                print("Invalid choice. Try again.")
   
def main():                                                                 #Entry point
    tree = FamilyTree()
    tree.generate_family()
    tree.run_program()

if __name__ == "__main__":
     main()
    