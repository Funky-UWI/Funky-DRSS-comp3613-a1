import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Review, Student, VoteCommand
from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    delete_user
)

from App.controllers.student import (
    create_student,
    get_students_by_name,
    get_student,
    get_all_students,
    get_all_students_json,
    update_student,
    delete_student,
)

from App.controllers.review import (
    create_review,
    update_review,
    delete_review,
    get_review,
    get_review_json,
    get_all_reviews,
    get_all_reviews_json,
    vote_review,
    # get_upvotes_by_review,
    # get_downvotes_by_review
)

from App.controllers.command import (
    create_vote_command,
    get_upvotes_by_review,
    get_downvotes_by_review,
    get_vote
)

from datetime import datetime

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_new_admin_user(self):
        user = User("bob", "bobpass", 2)
        assert user.access == 2

    # def test_new_normal_user(self):
    #     user = User("bob", "bobpass", 1)
    #     assert user.access == 1

    # def test_user_is_admin(self):
    #     user = User("bob", "bobpass", 2)
    #     assert user.is_admin()

    # def test_user_is_not_admin(self):
    #     user = User("bob", "bobpass", 1)
    #     assert not user.is_admin()

    # pure function no side effects or integrations called
    def test_to_json(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"access": 2, "id": None, "username": "bob"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

# Unit tests for Student model
class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("bob", "FST", "Computer Science")
        assert (
            student.name == "bob"
            and student.faculty == "FST"
            and student.programme == "Computer Science"
        )

    def test_student_to_json(self):
        student = Student("bob", "FST", "Computer Science")
        student_json = student.toJSON()
        self.assertDictEqual(
            student_json,
            {
                "faculty": "FST",
                "id": None,
                "karma": 0,
                "name": "bob",
                "programme": "Computer Science",
            },
        )


# Unit tests for Review model
class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review(1, 1, "good")
        assert review.student_id == 1 and review.user_id == 1 and review.text == "good"

    def test_review_to_json(self):
        review = Review(1, 1, "good")
        review_json = review.toJSON()
        self.assertDictEqual(
            review_json,
            {
                "id": None,
                "user_id": 1,
                "student_id": 1,
                "text": "good",
                "karma": 0,
                "num_upvotes": 0,
                "num_downvotes": 0,
            },
        )

class VoteCommandUnitTests(unittest.TestCase):
    # username = "rob"
    # password = "robpass"
    # access = 1
    # user = User(username, password, access)

    # name = "Bob"
    # faculty = "FST"
    # programme = "Comp Sci"
    # student = Student(name, faculty, programme)

    # review = Review(user_id=user.id, student_id=student.id, text="text")

    def test_votecommand_create(self):
        with self.subTest("Upvote"):
            vote = VoteCommand(1, 1, "upvote")
            assert vote.staff_id == 1 and vote.review_id == 1 and vote.vote_type == 1
        
        with self.subTest("Downvote"):
            vote = VoteCommand(1, 1, "downvote")
            assert vote.staff_id == 1 and vote.review_id == 1 and vote.vote_type == -1

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        test_user = create_user("john", "johnpass", 1)
        user = get_user_by_username("john")
        assert user.username == "john"

    def test_get_user(self):
        test_user = create_user("johnny", "johnpass", 1)
        user = get_user(test_user.id)
        assert test_user.username == user.username

    def test_get_all_users_json(self):
        users = get_all_users()
        users_json = get_all_users_json()
        assert users_json == [user.toJSON() for user in users]

    def test_update_user(self):
        user = create_user("danny", "johnpass", 1)
        update_user(user.id, "daniel")
        assert get_user(user.id).username == "daniel"

    def test_delete_user(self):
        user = create_user("bobby", "bobbypass", 1)
        uid = user.id
        delete_user(uid)
        assert get_user(uid) is None


# Integration tests for Student model
class StudentIntegrationTests(unittest.TestCase):
    def test_create_student(self):
        test_student = create_student("bob", "fst", "cs")
        student = get_student(test_student.id)
        assert test_student.name == student.name

    def test_get_students_by_name(self):
        students = get_students_by_name("bob")
        assert students[0].name == "bob"

    def test_get_all_students_json(self):
        students = get_all_students()
        students_json = get_all_students_json()
        assert students_json == [student.toJSON() for student in students]

    # tests updating a student's name, programme and/or faculty
    def test_update_student(self):
        with self.subTest("Update name"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, "bobby")
            assert get_student(student.id).name == "bobby"
        with self.subTest("Update programme"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, programme="it")
            assert get_student(student.id).programme == "it"
        with self.subTest("Update faculty"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, faculty="fss")
            assert get_student(student.id).faculty == "fss"
        with self.subTest("Update all"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, "bobby", "it", "fss")
            assert get_student(student.id).name == "bobby"
            assert get_student(student.id).programme == "it"
            assert get_student(student.id).faculty == "fss"

    def test_delete_student(self):
        student = create_student("bob", "fst", "cs")
        sid = student.id
        delete_student(sid)
        assert get_student(sid) is None

    def test_student_karma(self):
        staff = create_user("username3", "password", access=2)
        with self.subTest("No votes"):
            student = create_student("bob", "fst", "cs")
            review = create_review(student_id=student.id, user_id=1, text="good")
            self.assertEqual(student.get_karma(), 0)

        with self.subTest("1 upvote"):
            student = create_student("bob", "fst", "cs")
            review = create_review(student_id=student.id, user_id=1, text="good")
            vote = create_vote_command(review.id, 1, "upvote")
            self.assertEqual(student.get_karma(), 1)

        with self.subTest("1 downvote"):
            student = create_student("bob", "fst", "cs")
            review = create_review(student_id=student.id, user_id=1, text="good")
            vote = create_vote_command(review.id, 1, "downvote")
            self.assertEqual(student.get_karma(), -1)


# Integration tests for Review model
class ReviewIntegrationTests(unittest.TestCase):
    def test_create_review(self):
        staff = create_user("username2", "password", 2)
        student = create_student("name", "programme", "faculty")
        test_review = create_review(student.id, staff.id, "good")
        review = get_review(test_review.id)
        assert test_review.text == review.text

    def test_update_review(self):
        test_review = create_review(1, 1, "good")
        update_review(test_review.id, "bad")
        assert get_review(test_review.id).text == "bad"

    def test_delete_review(self):
        test_review = create_review(1, 1, "good")
        rid = test_review.id
        delete_review(rid)
        assert get_review(rid) is None

    def test_get_review_json(self):
        test_review = create_review(1, 1, "good")
        review_json = get_review_json(test_review.id)
        assert review_json == test_review.toJSON()

    def test_get_all_reviews_json(self):
        reviews = get_all_reviews()
        reviews_json = get_all_reviews_json()
        assert reviews_json == [review.toJSON() for review in reviews]

    def test_upvote_review(self):
        test_review = create_review(1, 1, "good")
        # upvote_review(test_review.id, 1)
        vote_review(test_review.id, 1, "upvote")
        assert get_review(test_review.id).get_num_upvotes() == 1

    def test_downvote_review(self):
        test_review = create_review(1, 1, "good")
        # downvote_review(test_review.id, 1)
        vote_review(test_review.id, 1, "downvote")
        assert get_review(test_review.id).get_num_downvotes() == 1

# Integration tests for Vote model
class VoteCommandIntegrationTests(unittest.TestCase):
    # # staff = create_user("rob", "robpass", access=1)
    # staff = get_user(1)
    # review = create_review(student_id=1, user_id=1, text="good")

    def test_create_votecommand(self):
        
        staff = create_user("username", "password", 2)
        student = create_student("name", "programme", "faculty")
        review = create_review(student_id=student.id, user_id=staff.id, text="good")

        with self.subTest("Upvote"):
            date = datetime.today()
            vote = create_vote_command(review_id=review.id, staff_id=staff.id, vote_type="upvote")
            self.assertDictEqual(
                vote.toJSON(),
                {
                    'id': vote.id,
                    'vote_type': 1,
                    'date': datetime.strftime(date, "%d/%m/%Y %H%:%M:%S"),
                    'review': review.toJSON(),
                    'staff': staff.toJSON()
                }
            )

        with self.subTest("Downvote"):
            date = datetime.today()
            vote = create_vote_command(review_id=review.id, staff_id=staff.id, vote_type="downvote")
            self.assertDictEqual(
                vote.toJSON(),
                {
                    'id': vote.id,
                    'vote_type': -1,
                    'date': datetime.strftime(date, "%d/%m/%Y %H%:%M:%S"),
                    'review': review.toJSON(),
                    'staff': staff.toJSON()
                }
            )

    def test_get_upvotes_by_review(self):   
        staff = get_user(1)
        student = create_student("name", "programme", "faculty")
        
        with self.subTest("0 votes"):
            review = create_review(student_id=student.id, user_id=staff.id, text="good")
            upvotes=get_upvotes_by_review(review.id)
            upvotes_json = [upvote.toJSON() for upvote in upvotes]
            self.assertEqual(upvotes, [])

        with self.subTest("1 Upvote"):
            review = create_review(student_id=student.id, user_id=staff.id, text="good")
            date = datetime.today()
            vote = create_vote_command(review_id=review.id, staff_id=staff.id, vote_type="upvote")
            upvotes = get_upvotes_by_review(review.id)
            self.assertListEqual(
                upvotes,
                [vote.toJSON()]
            )

        with self.subTest("2 Upvotes"):
            review = create_review(student_id=student.id, user_id=staff.id, text="good")
            date = datetime.today()
            upvote1 = create_vote_command(review_id=review.id, staff_id=staff.id, vote_type="upvote")
            upvote2 = create_vote_command(review_id=review.id, staff_id=staff.id, vote_type="upvote")
            upvotes = get_upvotes_by_review(review.id)
            self.assertListEqual(
                upvotes,
                [upvote1.toJSON(), upvote2.toJSON()]
            )
