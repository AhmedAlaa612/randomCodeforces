import requests
import random
import streamlit as st
from pymongo import MongoClient
import json

def fetch_and_store_problems(collection):
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            problems = data['result']['problems']
            for problem in problems:
                # Only insert if it doesn't already exist and has a rating
                if 'rating' in problem and not collection.find_one({"_id": str(problem['contestId']) + str(problem.get('index', ''))}):
                    problem['_id'] = str(problem['contestId']) + str(problem.get('index', ''))
                    collection.insert_one(problem)
            print("Problems fetched and stored in MongoDB.")
    else:
        print("Failed to fetch problems.")

# get random problem
def get_random_problem(minRating, maxRating, tags, tags_mode, collection):
    if tags_mode.lower() == "or":
        query = {
            "rating": {"$gte": minRating, "$lte": maxRating},
            "tags": {"$in": tags}
        }
    elif tags_mode.lower() == "and":
        query = {
            "rating": {"$gte": minRating, "$lte": maxRating},
            "tags": {"$all": tags}
        }
    matching_problems = list(collection.find(query))
    if matching_problems:
        return random.choice(matching_problems)
    else:
        return None

# get distinct tags
def get_distinct_tags(collection):
    return collection.distinct("tags")

# get min and max rating
def get_min_max_rating(collection):
    min_rating = collection.find_one(sort=[("rating", 1)])['rating']
    max_rating = collection.find_one(sort=[("rating", -1)])['rating']
    return min_rating, max_rating

contest_types = ['Educational', 'Global', 'Div. 1', 'Div. 2', 'Div. 3', 'Div. 4', 'April Fools', 'Hello', 'Good Bye']

# get contest (if type is "special" return contest not in contest_types) if Any return any contest, else return contest whose name contains the type
def get_random_contest(contest_types, contest_type, contests_collection):
    if contest_type == None:
        query = {}
    elif contest_type == "special":
        query = {"name": {"$not": {"$regex": "|".join(contest_types)}}}
    else:
        query = {"name": {"$regex": contest_type}}
    matching_contests = list(contests_collection.find(query))
    if matching_contests:
        return random.choice(matching_contests)
    else:
        return None
    
# connect to MongoDB
def connect_to_mongodb():
    client = MongoClient(st.secrets["mongo"]["uri"])
    db = client["codeforces"]
    problems = db["problems"]
    contests = db["contests"]
    return problems, contests