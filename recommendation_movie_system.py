#importing libraries
import requests
import json

#function definition for extracting all the dictionary from of data related to movie from tastedive api as per the user input.
def get_movies_from_tastedive(name):
    baseurl = 'https://tastedive.com/api/similar'
    para_dict = {'q': name, 'type': 'movies', 'limit': 20}
    page = requests.get(baseurl, params = para_dict)
    data = json.loads(page.text)
    return data


#Extracing only the title of movies from returned tastedive dict data. 
def extract_movie_titles(dic_data):
    movie_titles = []
    for each in dic_data['Similar']['Results']:
        movie_titles.append(each['Name'])
    return movie_titles


#Combining all the possible movie titles in a single list for output $ for parsing  it in next definition to get ratings. 
def get_related_titles(lst_movie_titles):
    combine_lst = []
    for each_movie in lst_movie_titles:
        Movies_lst = extract_movie_titles(get_movies_from_tastedive(each_movie))
        for movie in Movies_lst:
            if movie not in combine_lst:
                combine_lst.append(movie)
    return combine_lst


#parsing each particular movie from the list to get its rating if exists.
def get_movie_data(movie_title):
    baseurl = 'http://www.omdbapi.com/'
    para = {'apikey': 2080031, 't': movie_title, 'r':'json'}
    page = requests.get(baseurl , params = para)
    data = json.loads(page.text)
    return data


#Extracting the rating value
def get_movie_rating(dict_data):
    rating = dict_data['imdbRating']
    if len(rating) <= 0:
        rating = 'NA'
    else:
        rating = rating
    return rating


#output function designed for getting movies's name and ratings $ displaying them in the form of a list.
def get_sorted_recommendation(lst_movie):
    Movie_title = sorted(get_related_titles(lst_movie))
    ratings_lst = []
    for Movie in Movie_title:
        ratings_lst.append(get_movie_rating(get_movie_data(Movie)))
    recommended_movie = list(zip(Movie_title , ratings_lst))
    return recommended_movie

inp = input("Enter a movie/list of movie's that you have watched :").split(',')
result = get_sorted_recommendation(inp)
for each in result:
    print(each)

#Example inputs.
#print(get_sorted_recommendation(['Bridesmaids', 'Sherlock Holmes']))
#print(get_sorted_recommendation(["Black Panther", "Captain Marvel"]))
