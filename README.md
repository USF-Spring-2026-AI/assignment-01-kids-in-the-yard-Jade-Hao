# AI Assignment 01 - Kids in the Yard

# Overview
- Assignment 01 is centered around building a family tree. In this family tree we begin with two people born in 1950 (P generation), their children (F1 generation), their grandchildren(F2 generation) and so on. The tree will keep generating until there are no more children or until we reach the year 2120. The use of the family tree will be used in reporting the following:
    * Total Number of People in the tree 
    * Total number of people in the tree by Decade
    * Names duplicated
---
# Files Needed
- All CSV files: `first_names.csv`, `last_names.csv`, `life_expectancy.csv`, `rank_to_probaility.csv`, and `birth_and_marriage_rates.csv` --> undergraduate students did not have to use `gender_name_probability`.
---

# Files Included
- `person.py`: Represents individual - has first + last name, year of birth, death year, partner, children
- `person_factory.py`: Reads CSV files, assigns names using weighted probabilities, assigns death_year (based on plus/minus 10), creates partners based on marriage probability, and generates children based on birth rate ranges
- `family_tree.py`: Generate initial founders, recursively expand family tree, store all generated people, provide way to interact withthe  family tree. 
- `.gitignore`: Ignore pycache files
- [Assignment01-Reflection](https://github.com/USF-Spring-2026-AI/assignment-01-kids-in-the-yard-Jade-Hao/blob/main/Assignment01-%20Reflection.pdf)
---

# Notes to Run
- Must have all the files mentioned above
From terminal:
    python3 family_tree.py
---

# Comparison
1. Which tool(s) did you use?
- For this assignment, I heavily relied on GeeksforGeeks, W3Schools, StackOverflow, and a basic Google search. I have not coded in Python in a while, so this was used as a refresher. It also helps that I am taking Machine Learning with Professor Kelsey Urgo, so I am accustomed to some Python semantics as well as layout. As for LLM tools, I found myself having to refer to ChatGPT to break down some of the more complex tasks, as well as help me get a starting point within my assignment. I also found myself using GitHub Copilot while coding, since there is a Visual Studio Code extension. While coding, when I didn't have Copilot disabled, it would auto-complete my code without me having to do anything. It was strange, yet it made me feel more efficient since I was typing faster. However, it does get annoying due to the fact that it is guessing your next move and doesn’t have all the necessary information that we got from the PDF document. I often found myself double-checking anything it wrote out for me. For the most part, I did have to change things to fit my goals for this assignment. 

2. If you used an LLM, what was your prompt to the LLM?
- When I was using an LLM to start my code, I gave it the parameters: When I was using an LLM to start my code, I gave it the parameters: 
These are the files I have: Year Born: N/A , Year Died : life_expectancy.csv, First Name: first_names.csv, Last Name: Last_names.csv, rank_to_probability.csv, Partner / Spouse: birth_and__marriage_rates.csv, children : birth_and__marriage_rates.csv.
These are the 3 I want:
Person: The Person class is responsible for keepingdetails of each simulated person in the model.
PersonFactory: Reads data files + generates new instances of the person class
FamilyTree: The FamilyTree class is the “driver.”
Give me a skeleton Python program
from there. I copied the skeleton that it gave me to use as the foundation for this assignment.
For this comparison, I tested Gemini and ChatGPT by uploading the entire PDF to the prompt and noting that I am an undergraduate student. It further gave me a breakdown on what I had to do, and then I prompted it to give me all the code.

3. What differences are there between your implementation and the LLM?
- Found in the `LLM_code.py`, you can find the code. When comparing my code to the LLM, the code that I copied was from Gemini (ChatGPT was similar, but Gemini had better comments). One thing that I noticed from the get-go was how it put all the classes within one file. A style choice, but then it didn't requrie the use of `from ______ import ______`. Furthermore, it completely ignored the "rule" that we students were only to use the pandas library, it used `from collections import Counter`. Furthermore, the code seemed super short, it used calls that I am personally not familiar with, such as '.loc', '.iloc[0]', `.uniform()`. I also noticed how the logic and the variable names were vastly different from mine. There was some overlap, such as first_name/last_name however, the coding style was very on theme with the PEP 8 Style and was perfect in spacing and spelling. I also noticed how it didn't delve into as much detail as I did. Again, everything seemed very surface-level. Furthermore, there weren't as many `def` within the code. Per class, there were at most four and at least 2 `def` keywords. I also noticed that there were loops in here that I didn't even think about, such as a try/catch, as well as a call to a `DataFrame`, something that I didn't even think about before seeing this code. Overall, this limitation in detail shortened the code and gave way to complex shortcuts that I would have never done before.

4. What changes would you make to your implementation in general based on suggestions from the
LLM?
- I actually did make a change to my code, and that can be found with the life expectancy set to 75. Based on suggestions from the LLM, I wanted to improve my implementation by adding a check, such as verifying that a dataset row is not empty before accessing it. I think Machine Learning is getting to me, but I wanted to prevent runtime errors and wanted to double-check to make sure that my code could support missing or unexpected data. However, I think some changes I would want to make to my implementation in general, based on the LLM, would be to create a dictionary of lists. Playing around with the LLM further, I found that accessing a dictionary key is O(1), whereas Pandas  is O(n). This would make the tree generation faster and would help me practice thinking more about efficiency, since right now I feel my code is on the inefficient side. I think being able to understand how Python works to the extent that some LLMs know how it does would be super beneficial. Furthermore, I think being able to use variable names that are more easily recognizable and understandable would help me immensely. Sometimes, I name things similarly and end up confusing myself and overall making the readability of my code bad. I do recognize that some variable names that I have are the most intuitive, so seeing the different types of names that were generated really made me sit back and think about how and why I name the way I do.

5. What changes would you refuse to make?
- Some changes that I refused to make are centered around decisions and implementations that I have personally never seen before, and that don't follow the way I personally code. I think it was interesting to see what type of helper methods ChatGPT and Gemini used. I found most were ones that I have never heard of or are super niche.  Due to this, it doesn’t look like the way I code and lacks any personality. I also find that LLMs are not the best at following directions given in pdfs, they either skip over information or focus on one detail, overall skipping vital aspects that we discussed in class. As mentioned above, LLMs often overcomplicate things to a point where it would be impossible for a student to write. Overall, turning me off to make super big changes within my code. I do think LLMs are useful in the generation of ideas and a great tool to help you along the way, but I refuse to simply copy and paste code that I had no participation in. 

