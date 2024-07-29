import requests
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from flask_bootstrap import Bootstrap5
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,Float,desc


app = Flask(__name__)

app.secret_key = "secret_key"

Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_database.db"

db = SQLAlchemy(app)



class movie(db.Model):
    __tablename__ = "movie"
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    title:Mapped[str] = mapped_column(String,unique=True,nullable=False)
    year:Mapped[int] = mapped_column(Integer,nullable=False)
    description:Mapped[str] = mapped_column(String,nullable=False)
    rating:Mapped[float] = mapped_column(Float)
    ranking:Mapped[int] = mapped_column(Integer)
    review:Mapped[str] = mapped_column(String)
    image_url:Mapped[str] = mapped_column(String,nullable=False)


class edit_form(FlaskForm):
    rating = StringField("Your rating out of 10. E.g 7.5")
    review = StringField("Your review")
    submit = SubmitField("Done")

class add_form(FlaskForm):
    add_movie = StringField("Movie Title")
    submit = SubmitField("Add Movie")

with app.app_context():
    db.create_all()

def function_ranking(duplicate_ranking=False):
    all_movies = db.session.execute(db.select(movie).order_by(movie.rating.desc())).scalars()

    rating_occur_dict ={}

    for the_movie in all_movies:
        the_movie.ranking = 1

        for key in rating_occur_dict:
            if the_movie.rating == key:
                rating_occur_dict[key] += 1



        movie_rating_list = []
        movie_id_list = []
        movie_title_list = []
        all_movies_inner_loop = db.session.execute(db.select(movie).order_by(movie.rating.desc())).scalars()

        for moviee in all_movies_inner_loop:

            movie_rating_list.append(moviee.rating)
            movie_id_list.append(moviee.id)
            movie_title_list.append(moviee.title)
        for i in range(len(movie_rating_list)):
            print("\n\nThe begin;\n"
                  f"Movie_to_be_updated : {the_movie.title} - Its rating: {the_movie.rating} - Its ranking: {the_movie.ranking} "
                  f"Movie_to_be_compared: {movie_title_list[i]} - Its rating {movie_rating_list[i]}")
            if movie_rating_list[i] >= the_movie.rating and movie_id_list[i] != the_movie.id:
                if duplicate_ranking:
                    print("\n\nduplicate ranking enabled")
                    if movie_rating_list[i] == the_movie.rating:
                        pass
                    else:
                        if i != 0:
                            if not movie_rating_list[i] == movie_rating_list[i-1] :
                                the_movie.ranking += 1
                        elif i == 0:
                            the_movie.ranking += 1
                else:
                    if movie_rating_list[i] == the_movie.rating :
                        if i != 0:
                            if movie_rating_list[i] != movie_rating_list[i-1]:
                                keys = []
                                for key in rating_occur_dict:
                                    keys.append(key)
                                if the_movie.rating not in keys:
                                    print("key not found.good to go")
                                    rating_occur_dict[the_movie.rating] = 1
                                print(rating_occur_dict[the_movie.rating])
                                the_movie.ranking += rating_occur_dict[the_movie.rating]

                    else:
                        the_movie.ranking += 1

            print("\nThe end:\n"
                f"Movie_to_be_updated : {the_movie.title} - Its rating: {the_movie.rating} - Its ranking: {the_movie.ranking} "
                f"Movie_to_be_compared: {movie_title_list[i]} - Its rating {movie_rating_list[i]}")
        db.session.commit()



@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        print("post")
        function_ranking(duplicate_ranking=True)
    else:
        print("get")
        function_ranking()
    all = db.session.execute(db.select(movie).order_by(desc(movie.ranking))).scalars()
    return render_template("index.html",movies=all)


@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    edit= edit_form()
    if request.method == "POST":
        rating = edit.rating.data
        review = edit.review.data
        movie_to_edit = db.session.execute(db.select(movie).where(movie.id==id)).scalar()
        if rating != "":
            movie_to_edit.rating = float(rating)

# ----------------------------------- ranking ---------------------------------------------------------------- #

# ------------------------------------ ranking ----------------------------------------------------------------- #
        if review != "":
            movie_to_edit.review = review

        db.session.commit()

        return redirect(url_for('home'))
    return render_template("edit.html",form=edit,id=id)

@app.route("/delete/<int:id>")
def delete(id):
    movie_to_delete = db.session.execute(db.select(movie).where(movie.id==id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add-movie",methods=["GET","POST"])
def add_movie():
    add_movie = add_form()
    if request.method == "POST":
        movie_name = add_movie.add_movie.data

        movies = requests.get(f"https://www.omdbapi.com/?s={movie_name}&apikey=37f1822c").json()['Search']

        return render_template("select.html",movies=movies)
    return render_template("add.html",add_movie=add_movie)

@app.route("/select-movie")
def select_movie():
    title = request.args.get('title')
    year = request.args.get('year')
    poster = request.args.get('poster')
    new_movie = movie(title=title,year=year,image_url=poster,description=title)
    db.session.add(new_movie)
    db.session.commit()

    selected_movie = db.session.execute(db.select(movie).where(movie.title==title)).scalar()

    return redirect(url_for('edit',id=selected_movie.id))




if __name__ == "__main__":
    app.run(debug=True)
