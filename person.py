class Person:
    """
    Represnts a person with basic person + family information
    """
    def __init__(self, first_name, last_name, gender, year_of_birth, death_year=None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender 
        
        self.year_of_birth = year_of_birth
        self.death_year = death_year
        
        self.partner = None
        self.children = []
    
    def get_full_name(self):                                # Returns individuals full name
        return f"{self.first_name} {self.last_name}"

    def get_year_of_birth(self):
        return self.year_of_birth
    
    def get_death_year(self):                               #Will return None if still alive
        return self.death_year
    
    def get_partner(self):
        return self.partner

    def get_children(self):
        return self.children
    
    def set_partner(self, partner):                          #Partner = Object
        self.partner = partner

    def add_child(self,child):
        self.children.append(child)
    
    def set_death_year(self, death_year):                   #Year of death = int
        self.death_year = death_year
