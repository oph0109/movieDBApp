#
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

    def __init__(self, MID, T, Rls_Yr):
        self._Movie_ID = MID
        self._Title = T
        self._Release_Year = Rls_Yr

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Year(self):
        return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:

    def __init__(self, MID, T, Rls_Yr, Num_Rvw, Avg_R):
        self._Movie_ID = MID
        self._Title = T
        self._Release_Year = Rls_Yr
        self._Num_Reviews = Num_Rvw
        self._Avg_Rating = Avg_R

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Year(self):
        return self._Release_Year

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

    def __init__(self, MID, T, RD, R, O, B, RV, NR, AR, TL, G, PC):
        self._Movie_ID = MID
        self._Title = T
        self._Release_Date = RD
        self._Runtime = R
        self._Original_Language = O
        self._Budget = B
        self._Revenue = RV
        self._Num_Reviews = NR
        self._Avg_Rating = AR
        self._Tagline = TL
        self._Genres = G
        self._Production_Companies = PC

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Date(self):
        return self._Release_Date

    @property
    def Runtime(self):
        return self._Runtime

    @property
    def Original_Language(self):
        return self._Original_Language

    @property
    def Budget(self):
        return self._Budget

    @property
    def Revenue(self):
        return self._Revenue

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating

    @property
    def Tagline(self):
        return self._Tagline

    @property
    def Genres(self):
        return self._Genres

    @property
    def Production_Companies(self):
        return self._Production_Companies


def printDetails(movie):
    print(movie.Movie_ID)
    print(movie.Title)
    print(movie.Release_Date)
    print(movie.Runtime)
    print(movie.Original_Language)
    print(movie.Budget)
    print(movie.Revenue)
    print(movie.Num_Reviews)
    print(movie.Avg_Rating)
    print(movie.Tagline)
    print(movie.Genres)
    print(movie.Production_Companies)


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
    try:
        sql = "SELECT COUNT(Movie_ID) FROM Movies"
        return datatier.select_one_row(dbConn, sql)[0]
    except Exception:
        return -1


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    try:
        sql = "SELECT COUNT(Rating) FROM Ratings"
        return datatier.select_one_row(dbConn, sql)[0]
    except Exception:
        return -1


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
    sql = "SELECT Movie_ID, Title, strftime('%Y', DATE(Release_Date)) FROM Movies WHERE Title LIKE '" + pattern + "' ORDER BY Title"
    list = []
    for i in datatier.select_n_rows(dbConn, sql):
        movie = Movie(i[0], i[1], i[2])
        list.append(movie)
    return list


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
    if (movie_exists(dbConn, movie_id)):
        sql = "SELECT Movies.Movie_ID, Title, DATE(Release_Date), Runtime, Original_Language, Budget, Revenue, COUNT(Rating), Movie_Taglines.Tagline FROM Movies LEFT JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID LEFT JOIN Movie_Taglines ON Movies.Movie_ID = Movie_Taglines.Movie_ID WHERE Movies.Movie_ID = '" + str(
            movie_id) + "'"
        details = datatier.select_one_row(dbConn, sql)
        sql = "SELECT Genres.Genre_Name FROM Genres INNER JOIN Movie_Genres ON Genres.Genre_ID = Movie_Genres.Genre_ID INNER JOIN Movies ON Movie_Genres.Movie_ID = Movies.Movie_ID WHERE Movies.Movie_ID = '" + str(
            movie_id) + "' ORDER BY Genres.Genre_Name"
        genres = []
        for i in datatier.select_n_rows(dbConn, sql):
            genres.append(i[0])
        sql = "SELECT Company_Name FROM Companies INNER JOIN Movie_Production_Companies ON Companies.Company_ID = Movie_Production_Companies.Company_ID INNER JOIN Movies ON Movie_Production_Companies.Movie_ID = Movies.Movie_ID WHERE Movies.Movie_ID = '" + str(
            movie_id) + "' ORDER BY Company_Name"
        companies = []
        for i in datatier.select_n_rows(dbConn, sql):
            companies.append(i[0])
        sql = "SELECT COALESCE(SUM(Rating),0) FROM Ratings WHERE Movie_ID = '" + str(
            movie_id) + "'"
        total_rating = datatier.select_one_row(dbConn, sql)[0]
        if (details[7] != 0):
            avg_rating = total_rating / details[7]
        else:
            avg_rating = 0
        if (details[8] == None):
            movie = MovieDetails(details[0], details[1], details[2],
                                 details[3], details[4], details[5],
                                 details[6], details[7], avg_rating, "",
                                 genres, companies)
        else:
            movie = MovieDetails(details[0], details[1], details[2],
                                 details[3], details[4], details[5],
                                 details[6], details[7], avg_rating,
                                 details[8], genres, companies)
        return movie
    else:
        return None


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    sql = "SELECT Movies.Movie_ID, Title, strftime('%Y',DATE(Release_Date)), COUNT(Rating) as NumReviews, AVG(Rating) FROM Movies INNER JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID GROUP BY Movies.Movie_ID HAVING NumReviews >= " + str(
        min_num_reviews) + " ORDER BY AVG(Rating) DESC LIMIT " + str(N)
    topN = []
    for i in datatier.select_n_rows(dbConn, sql):
        movie = MovieRating(i[0], i[1], i[2], i[3], i[4])
        topN.append(movie)
    if len(topN) != 0:
        return topN
    else:
        return []


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    if (movie_exists(dbConn, movie_id)):
        sql = "INSERT INTO Ratings (Movie_ID, Rating) VALUES (" + str(
            movie_id) + ", " + str(rating) + ");"
        datatier.perform_action(dbConn, sql)
        return 1
    else:
        return 0


def movie_exists(dbConn, movie_id):
    sql = "SELECT Movie_ID FROM Movies WHERE Movie_ID = " + str(movie_id)
    m_exists = len(datatier.select_one_row(dbConn, sql)) == 1
    return m_exists


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    sql = "SELECT Movie_ID FROM Movies WHERE Movie_ID = ?"
    if len(datatier.select_one_row(dbConn, sql, [movie_id])) == 0:
      return 0
    sql = "SELECT Movie_ID FROM Movie_Taglines WHERE Movie_ID = '" + str(
        movie_id) + "'"
    if len(datatier.select_one_row(dbConn, sql)) != 0:
        sql = "UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?"
        datatier.perform_action(dbConn, sql, [tagline, movie_id])
        return 1
    else:
        sql = "INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?);"
        datatier.perform_action(dbConn, sql,[movie_id, tagline])
        return 1
    return 0
