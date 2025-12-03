from datetime import datetime
import uuid


class User:
    def __init__(self, user_name):
        self._user_name = user_name
        self._reviews = {}
        self._ratings = {}
        self.__id = str(uuid.uuid4())

    @property
    def id(self):
        return self.__id
        
    @property
    def user_name(self):
        return self._user_name
    
    @property
    def reviews(self):
        return self._reviews
    
    @property
    def ratings(self):
        return self._ratings

    def write_review(self, movie, text):
        #if the review is empty or there are just spaces
        if not text or not text.strip():
            raise ValueError("Review can't be empty!")
        #creating new review
        review = Review(user_id=self.id, #id of the current user
                        movie_id=movie.id, #id of the movie
                        review_text=text.strip()) #text for the review
        
        self._reviews[review.review_id] = review #saving the review object under the key of its ID

        movie.add_review(review) #saving the review for the movie
        return f"The review is added at {review.date.strftime('%d-%m-%Y %H:%M')}"

    def update_review(self, review_id, new_text):
        if not new_text or not new_text.strip():
            raise ValueError("New text can't be empty!")
        if review_id not in self._reviews: #checking if review is not exist
            raise KeyError("The review is not found!")
        review = self._reviews[review_id]
        review.review_text = new_text.strip()

    def delete_review(self, review_id, movie):
        if review_id not in self.reviews: #checking if the review doesn't exist
            raise KeyError("The review is not found!")
        self.reviews.pop(review_id) #deleteing the last review from the dictionary from the user
        movie.reviews.pop(review_id, None) #deleting the last review from the movie. None - to prevent the error

    def rate_movie(self, movie, score):
        # creating rating
        rating = Rating(movie_id=movie.id, 
                        user_id=self.id, 
                        score=score)
        self._ratings[movie.id] = rating
        movie.add_rating(rating)
        return rating

class Media:
    def __init__(self, name: str, genre: str):
        self._id = str(uuid.uuid4())
        self._name = name
        self._genre = genre

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def genre(self):
        return self._genre
    
class Movie(Media):
    def __init__(self, name, genre, rating, year):
        super().__init__(name, genre)
        self._rating = rating
        self._year = year 
        self._reviews = {}
        self._ratings = {}
        self._average_rating = None

    @property
    def rating(self):
        return self._rating
    
    @property
    def year(self):
        return self._year
    
    @property
    def reviews(self):
        return self._reviews
    
    @property
    def average_rating(self):
        return self._average_rating

    def add_review(self, review):
        self._reviews[review.review_id] = review #saving the review object under the key of its ID

    def remove_review(self, review_id):
        self._reviews.pop(review_id, None)

    def add_rating(self, rating):
        # creating rating
        self._ratings[rating.user_id] = rating
        # calculating average
        self._recompute_average()

    def _recompute_average(self):
        if self._ratings:
            self._average_rating = sum(r.score for r in self._ratings.values()) / len(self._ratings)
        else:
            self._average_rating = None

class Review:
    def __init__(self, user_id, movie_id, review_text):
        if not review_text or not review_text.strip():
            raise ValueError("Review cannot be empty")

        self.__review_id = str(uuid.uuid4())
        self._user_id = user_id
        self._movie_id = movie_id
        self._date = datetime.utcnow() #the date when user left the review
        self._review_text = review_text.strip()

    @property
    def review_id(self):
        return self.__review_id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def movie_id(self):
        return self._movie_id
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Date should be a datetime object!")
        self._date = value

    @property
    def review_text(self):
        return self._review_text
    
    @review_text.setter
    def review_text(self, value):
        if not value or not value.strip():
            raise ValueError("Review can't be empty!")
        self._review_text = value.strip() #cutting the spaces
        self._date = datetime.utcnow() #when the text is editing - the date is also editing

class Rating:
    def __init__(self, movie_id, user_id, score):
        self.__rating_id = str(uuid.uuid4())
        self._movie_id = movie_id
        self._user_id = user_id
        self.score = score
        self._date = datetime.utcnow() #the date when user rated the movie

    @property
    def rating_id(self):
        return self.__rating_id
    
    @property
    def movie_id(self):
        return self._movie_id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Score should be a number!")
        value = int(value) #if it's float doing it int
        if not (1 <= value <= 10):
            raise ValueError("Score should be 1-10")
        self._score = value
    
    @property
    def date(self):
        return self._date

if __name__ == "__main__":
    movie = Movie("The Matrix", "Sci-Fi", None, 1999)
    user = User("Alice")

    print(user.write_review(movie, "Great movie!"))
    print("Amount of reviews:", len(movie.reviews))

    review_id = list(user.reviews.keys())[0]
    user.update_review(review_id, "Amazing film!")
    print("Updated review:", user.reviews[review_id].review_text)
