import objecttier
import sqlite3

dbConn = sqlite3.connect("MovieLens.db")
print("** Welcome to the MovieLens app **\n")

print("General stats:")
print("  # of movies: " + f"{objecttier.num_movies(dbConn):,}")
print("  # of reviews: " + f"{objecttier.num_reviews(dbConn):,}")
while (1):
    print()
    choice = input("Please enter a command (1-5, x to exit): ")
    if choice == '1':
        print()
        title = input("Enter movie name (wildcards _ and % supported): ")
        list = objecttier.get_movies(dbConn, title)

        print("\n# of movies found: " + f"{len(list)}")
        if len(list) <= 100:
            print()
            for i in list:
                print(f"{i.Movie_ID}" + " : " + f"{i.Title}" + " (" +
                      f"{i.Release_Year}" + ")")
        else:
            print(
                "\nThere are too many movies to display, please narrow your search and try again..."
            )
    elif choice == '2':
        print()
        id = input("Enter movie id: ")
        print()
        movie = objecttier.get_movie_details(dbConn, id)
        if movie != None:
            print(f"{movie.Movie_ID}" + " : " + f"{movie.Title}" +
                  "\n  Release date: " + f"{movie.Release_Date}" +
                  "\n  Runtime: " + f"{movie.Runtime}" + " (mins)"
                  "\n  Orig language: " + f"{movie.Original_Language}" +
                  "\n  Budget: $" + f"{movie.Budget:,}" + " (USD)" +
                  "\n  Revenue: $" + f"{movie.Revenue:,}" + " (USD)" +
                  "\n  Num reviews: " + f"{movie.Num_Reviews}" +
                  "\n  Avg rating: ",
                  end="")
            print("%.2f" % round(movie.Avg_Rating, 2), end="")
            print(" (0..10)")
            print("  Genres: ", end="")
            for i in movie.Genres:
                print(i, end=", ")
            print()
            print("  Production companies: ", end="")
            for i in movie.Production_Companies:
                print(i, end=", ")
            print()
            print("  Tagline: " + f"{movie.Tagline}")
        else:
            print("No such movie...")
    elif choice == '3':
        print()
        numMovies = int(input("N? "))
        if numMovies >= 1:
            numReviews = int(input("min number of reviews? "))
            if numReviews >= 1:
                print()
                for i in objecttier.get_top_N_movies(dbConn, numMovies,
                                                     numReviews):
                    print(
                        f"{i.Movie_ID} : {i.Title} ({i.Release_Year}), avg rating = ",
                        end="")
                    print("%.2f" % round(i.Avg_Rating, 2), end="")
                    print(f" ({i.Num_Reviews} reviews)")
            else:
                print(
                    "Please enter a positive value for min number of reviews..."
                )
        else:
            print("Please enter a positive value for N...")
    elif choice == '4':
        print()
        
        rating = int(input("Enter rating (0..10): "))
        if rating <= 10 and rating >= 0:
            id = input("Enter movie id: ")
            if(objecttier.add_review(dbConn, id, rating) == 1):
              print("\nReview successfully inserted")
            else:
              print("\nNo such movie...")
        else:
            print("Invalid rating...")
    elif choice == '5':
        print()
        tagline = input("tagline? ")
        id = input("movie id? ")
        if objecttier.get_movie_details(dbConn, id) != None:
            objecttier.set_tagline(dbConn, id, tagline)
            print("\nTagline successfully set")
        else:
            print("\nNo such movie...")
    elif choice == 'x':
        exit(0)
