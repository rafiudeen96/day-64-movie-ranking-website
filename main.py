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
    rating:Mapped[float] = mapped_column(Float,nullable=False)
    ranking:Mapped[int] = mapped_column(Integer,nullable=False)
    review:Mapped[str] = mapped_column(String,nullable=False)
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

@app.route("/")
def home():
    all_movies = db.session.execute(db.select(movie).order_by(desc(movie.ranking))).scalars()
    return render_template("index.html",movies=all_movies)

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    edit= edit_form()
    if request.method == "POST":
        rating = edit.rating.data
        review = edit.review.data
        movie_to_edit = db.session.execute(db.select(movie).where(movie.id==id)).scalar()
        if rating != "":
            movie_to_edit.rating = float(rating)
            movie_to_edit.ranking = 1

# ----------------------------------- ranking ---------------------------------------------------------------- #
            all_movies = db.session.execute(db.select(movie).order_by(movie.ranking)).scalars()
            movie_rating_list = []
            for moviee in all_movies:
                movie_rating_list.append(moviee.rating)
            for i in range(len(movie_rating_list)):
                if movie_rating_list[i] > movie_to_edit.rating:
                    if i == len(movie_rating_list)-1:
                        movie_to_edit.ranking += 1
                    else:
                        if movie_rating_list[i] != movie_rating_list[i+1]:
                            movie_to_edit.ranking += 1
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

        tmdb_url = "https://api.themoviedb.org/3/search/movie"

        params = {"query":movie_name,
                  "api_key":"d2d05f3b50a79057c5dc0111b82f38f9"}

        movies = requests.get(tmdb_url,params).json()["results"]

        return render_template("select.html",movies=movies)
    return render_template("add.html",add_movie=add_movie)

@app.route("/select-movie/<movie_data>")
def select_movie(movie_data):
    return movie_data['original_title']




if __name__ == "__main__":
    app.run(debug=True)
