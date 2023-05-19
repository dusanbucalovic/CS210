import math
from collections import defaultdict
from collections import Counter

# Team members: Amit Patel, Zayaan Syed, Dusan Bucalovic, Emanuel Meshoyrer

# You may not add any other imports

# For each function, replace "pass" with your code

# --- TASK 1: READING DATA ---

# 1.1
def read_ratings_data(f):
    ratingFile = open(f, "r")
    ratings = []
    for line in ratingFile:
        ratings.append(line.strip())
    ratingFile.close()

    ratingDictionary = {}
    for line in ratings:
        rating = line.split("|")
        movieName = rating[0].strip()
        movieRating = float(rating[1].strip())

        if movieName not in ratingDictionary:
            ratingDictionary[movieName] = []
        
        ratingDictionary[movieName].append(movieRating)

    return ratingDictionary

# 1.2
def read_movie_genre(f):
    genreFile = open(f, "r")
    genres = []
    for line in genreFile:
        genres.append(line.strip())
    genreFile.close()

    movieGenreDictionary = {}
    for line in genres:
        genre = line.split("|")
        movieName = genre[2].strip()
        movieGenre = genre[0].strip()
        
        movieGenreDictionary[movieName] = movieGenre

    return movieGenreDictionary

# --- TASK 2: PROCESSING DATA ---

# 2.1
def create_genre_dict(d):
    genreDictionary = {}

    for movie in d:
        genre = d[movie]
        
        if genre not in genreDictionary:
            genreDictionary[genre] = []
        
        genreDictionary[genre].append(movie)

    return genreDictionary

# 2.2
def calculate_average_rating(d):
    averageRatingDictionary = {}

    for movie in d:
        ratings = d[movie]

        averageRating = round(sum(ratings) / len(ratings), 1)
        averageRatingDictionary[movie] = averageRating

    return averageRatingDictionary

# --- TASK 3: RECOMMENDATION ---

# 3.1
def get_popular_movies(d, n=10):
    popularMovies = sorted(d.items(), key = lambda x:x[1], reverse=True)
    
    return dict(popularMovies[:n])

# 3.2
def filter_movies(d, thres_rating=3.0):
    filterThres = {}
    for movieName, filterRating in d.items():
        if filterRating >= thres_rating:
            filterThres[movieName] = filterRating

    return filterThres

# 3.3
def get_popular_in_genre(genre, genreDictionary, genre_to_movies, movie_to_average_rating, n=5):
    genreMoviesDictionary = {}
    genreDict = {}
    # find movies in genre
    allMovies = genre_to_movies[genre]
    for movies in allMovies:
        genreMoviesDictionary[movies] = movie_to_average_rating[movies]
        genreDict = dict(sorted(genreMoviesDictionary.item(), key=lambda item: item[1], reverse=True))[:n]


    if n < len(genreDictionary):
        for movies in genreDictionary:
            i = 0
            if i == n:
                break
                genreMoviesDictionary[movies] = movie_to_average_rating[movies]
            genreDict = dict(sorted(genreMoviesDictionary.item(), key=lambda item: item[1], reverse=True))
            i += 1

    return genreDict

# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    ratingDictionary = {}
    ratingDict = {}

    # find movies in genre
    allMoviesGenre = genre_to_movies[genre]
    for movies in allMoviesGenre:
        ratingDictionary[movies] = movie_to_average_rating[movies]
        ratingDict = calculate_average_rating(ratingDictionary)

    return ratingDict
# 3.5
def genre_popularity(genreDictionary, genre_to_movies, movie_to_average_rating, n=5):
    genrePopularity = {}
    for key in genreDictionary:
        if key not in genrePopularity:
            genrePopularity[key] = get_genre_rating(key, genreDictionary, genre_to_movies, movie_to_average_rating)
    if len(genrePopularity) > n:
        return get_popular_movies(genrePopularity, len(genrePopularity))[:n]
    else:
        return get_popular_movies(genrePopularity)

# --- TASK 4: USER FOCUSED ---

# 4.1
def read_user_ratings(f):
    file=open(f)
    dic={}
    r=file.readlines()
    n=len(r)
    count=0

    for x in r:
        path=x.split('|')
        user = path[2].strip()
        l = (path[0], path[1])
        count = count+1
           
        if user not in dic:
            dic[user]=[]
        
        dic[user].append(l)

    return dic

# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    movies = user_to_movies[user_id]
    movie_names = []
    
    genre_rating = {}
    for i in movies:
        movie_names.append(i[0])
        genre = movie_to_genre[i[0]]
        rating = i[1]
        if genre not in genre_rating:
            genre_rating[genre] = [float(rating), 1]
        else:
            genre_rating[genre][0] += float(rating)
            genre_rating[genre][1] += 1

    user_genre_average_rating = {}
    for f, k in genre_rating.items():
        user_genre_average_rating[f] = k[0] / k[1]

    top_genre = max(user_genre_average_rating, key=user_genre_average_rating.get)

    return top_genre

# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    movies = user_to_movies[user_id]
    movie_names = []
    
    genre_rating = {}
    for i in movies:
        movie_names.append(i[0])
        genre = movie_to_genre[i[0]]
        rating = i[1]
        if genre not in genre_rating:
            genre_rating[genre] = [float(rating), 1]
        else:
            genre_rating[genre][0] += float(rating)
            genre_rating[genre][1] += 1

    user_genre_average_rating = {}
    for f, k in genre_rating.items():
        user_genre_average_rating[f] = k[0] / k[1]

    top_genre = max(user_genre_average_rating, key=user_genre_average_rating.get)

    movies_in_top_genre = []

    for movie in movie_to_genre:
        if (movie_to_genre[movie] == top_genre):
            movies_in_top_genre.append(movie)

    movies_top_genre_rating = []
    for movie in movies_in_top_genre:
        if (movie in movie_names):
            continue
        
        movie_rating = movie_to_average_rating[movie]
        movies_top_genre_rating.append((movie, movie_rating))

    movies_top_genre_rating.sort(key = lambda x: -x[1])
    top_movies = movies_top_genre_rating

    return_dict = {}
    counter = 0
    for movie_with_rating in top_movies:
        if (counter > 2):
            break
        return_dict[movie_with_rating[0]] = movie_with_rating[1]
        
    return return_dict

# --- main function for your testing ---
def main():
    ratingDictionary = read_ratings_data("movieRatingSample.txt")
    movieGenreDictionary = read_movie_genre("genreMovieSample.txt")

    genreDictionary = create_genre_dict(movieGenreDictionary)
    averageRatingDictionary = calculate_average_rating(ratingDictionary)

    userRatingsDictionary = read_user_ratings("movieRatingSample.txt")

    top_genre = get_user_genre("6", userRatingsDictionary, movieGenreDictionary)

    userRecDictionary = recommend_movies("6", userRatingsDictionary, movieGenreDictionary, averageRatingDictionary)

main()