import pytest
from main import User, Movie, Review, Rating

@pytest.fixture
def setup_objects():
    user = User("Alice")
    movie = Movie("The Matrix", "Sci-Fi", None, 1999)
    return user, movie

# ---------------------- HAPPY PATH TESTS ---------------------- #

def test_write_review(setup_objects):
    user, movie = setup_objects
    msg = user.write_review(movie, "Great movie!")
    assert "The review is added at" in msg #checking that the message has been confirmed by adding a review
    assert len(user.reviews) == 1 #checking that user has 1 review
    assert len(movie.reviews) == 1 #checking that movie has 1 review


def test_update_review(setup_objects):
    user, movie = setup_objects
    user.write_review(movie, "Good")
    review_id = list(user.reviews.keys())[0] #getting the id of the created review

    user.update_review(review_id, "Amazing film!")
    assert user.reviews[review_id].review_text == "Amazing film!" #checking that the review updated


def test_delete_review(setup_objects):
    user, movie = setup_objects
    user.write_review(movie, "Nice")
    review_id = list(user.reviews.keys())[0]

    user.delete_review(review_id, movie)
    assert len(user.reviews) == 0
    assert len(movie.reviews) == 0


def test_rate_movie(setup_objects):
    user, movie = setup_objects
    rating = user.rate_movie(movie, 8)
    assert rating.score == 8
    assert movie.average_rating == 8


def test_multiple_ratings_average():
    user1 = User("Alice")
    user2 = User("Bob")
    movie = Movie("Inception", "Sci-Fi", None, 2010)

    user1.rate_movie(movie, 8)
    user2.rate_movie(movie, 10)

    assert movie.average_rating == 9


# ---------------------- ERROR / EDGE CASES ---------------------- #

def test_empty_review_error(setup_objects):
    user, movie = setup_objects
    with pytest.raises(ValueError):
        user.write_review(movie, "")
    with pytest.raises(ValueError):
        user.write_review(movie, "   ")


def test_update_nonexistent_review(setup_objects):
    user, movie = setup_objects
    with pytest.raises(KeyError):
        user.update_review("no_such_id", "text")


def test_delete_nonexistent_review(setup_objects):
    user, movie = setup_objects
    with pytest.raises(KeyError): #keyerror because such id is npt exist
        user.delete_review("wrong_id", movie)


def test_invalid_rating_type(setup_objects):
    user, movie = setup_objects
    with pytest.raises(TypeError):
        user.rate_movie(movie, "not_number")


def test_rating_out_of_bounds(setup_objects):
    user, movie = setup_objects
    with pytest.raises(ValueError):
        user.rate_movie(movie, 0)
    with pytest.raises(ValueError):
        user.rate_movie(movie, 11)
