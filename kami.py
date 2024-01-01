import pandas as pd
import os 
from dotenv import load_dotenv #used to read .env files
import random
from discord.ext import commands, tasks

# Load environment variables from .env
load_dotenv()
#saves the values attribute to csv_path from the csv_path variable in .env file
csv_path = os.getenv('csv_path') 
# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_path)
# Iterate through each row in the DataFrame
list = []
for index, row in df.iterrows():
    # Access the values in each column
    name = row['Name']
    description = row['description']
    imageUrl = row['imageUrl']

    
    # Store the facts related to each name (you can customize this part based on your specific use case)
    facts = {
        'Name': name,
        'Description': description,
    }
    list.append(facts)
    # You can perform further processing or store the facts in a data structure of your choice (e.g., a list, dictionary, database, etc.)

#function for accessing random charcters and info
def get_random_character(list):
    return random.choice(list)

def get_list():
    return list

#function for accessing a charcter and info
def get_character(list, name):
    #name = str(name).title()
    for dict in list:
        if name == dict['Name']: 
            name = dict['Name']
            description = dict['Description']
            return description 
    else:
        msg = "Try typing the name differently, for Android eighteen: Android 18"
        description = "Wrong name"
        return description + msg 
    

print(get_character(list, "Goku"))