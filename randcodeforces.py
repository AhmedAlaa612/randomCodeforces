import streamlit as st
from utils import *

contest_types = ['Educational', 'Global', 'Div. 1', 'Div. 2', 'Div. 3', 'Div. 4', 'April Fools', 'Hello', 'Good Bye']
# connect to the database
problems, contests = connect_to_mongodb()

# navigation bar problems and contests pages
page = st.sidebar.radio("What do you want?", ["Random Problem", "Random Contest"])

if page == "Random Problem":
    # Define the tags, ratings, and logical operators
    tags = get_distinct_tags(problems)
    min_rating, max_rating = get_min_max_rating(problems)
    logical_operators = ["AND", "OR"]

    # Streamlit app layout
    st.title("Random Codeforces Problem")

    selected_tags = st.pills("Select Tags", tags, selection_mode="multi")
    rating_range = st.slider("Select Rating Range", min_rating, max_rating, (min_rating, max_rating), label_visibility="hidden")
    logical_operator = st.radio("Operator", logical_operators, horizontal=True, label_visibility="hidden")

    if st.button("Find Problem"):
        problem = get_random_problem(rating_range[0], rating_range[1], selected_tags, logical_operator, problems)
        if problem:
            st.write("Here is a problem for you:")
            st.link_button(problem['_id'] + "  :  " + problem['name'] + "   (Rating: " + str(problem['rating']) + ")", f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem.get('index', '')}")
            st.write(problem)
        else:
            st.write("No problems found with the selected criteria.")

elif page == "Random Contest":
    # Streamlit app layout
    st.title("Random Codeforces Contest")
    selected_type = st.pills("Select Tags", contest_types + ['special'])
    if st.button("Find Contest"):
        contest = get_random_contest(contest_types, selected_type, contests)
        if contest:
            st.write("Here is a contest for you:")
            st.link_button(contest['name'], f"https://codeforces.com/contest/{contest['id']}")
            st.write(contest)
        else:
            st.write("No contests found.")
    