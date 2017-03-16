import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Post

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_follow(self):
		u1 = User(nickname='thanh', email='thanh@gmail.com')
		u2 = User(nickname='trinh', email='trinh@gmail.com')
		db.session.add(u1)
		db.session.add(u2)
		assert u1.unfollow(u2) is None
		u = u1.follow(u2)
		db.session.add(u)
		db.session.commit()
		assert u1.follow(u2) is None
		assert u1.is_following(u2)
		assert u1.followed.count() == 1
		assert u1.followed.first().nickname == 'trinh'
		assert u2.followers.count() == 1
		assert u2.followers.first().nickname == 'thanh'
		u = u1.unfollow(u2)
		assert u is not None
		db.session.add(u)
		db.session.commit()
		assert not u1.is_following(u2)
		assert u1.followed.count() == 0
		assert u2.followers.count() == 0

if __name__ == '__main__':
	unittest.main()