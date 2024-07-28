# movie_list = [["Phone Booth",2002,
#     "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     7.3,
#     10,
#     "My favourite character was the caller.",
#     "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"],["Avatar The Way of Water",
#     2022,
#     "Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     7.3,
#     9,
#     "I liked the water.",
#     "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"]]
#
# with app.app_context():
#     for movie_data in movie_list:
#         new_movie = movie(title=movie_data[0],year=movie_data[1],description=movie_data[2],rating=movie_data[3],
#                           ranking=movie_data[4],review=movie_data[5],image_url=movie_data[6])
#         db.session.add(new_movie)
#         db.session.commit()
