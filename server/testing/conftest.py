#!/usr/bin/env python3

import pytest
from app import app
from models import db, Article, User

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(autouse=True)
def setup_test_data():
    with app.app_context():
        db.create_all()
        
        # Create test user
        user = User(username='testuser')
        db.session.add(user)
        
        # Create test articles
        article1 = Article(
            author='Test Author',
            title='Member Only Article',
            content='This is member only content',
            preview='This is...',
            minutes_to_read=5,
            is_member_only=True
        )
        
        article2 = Article(
            author='Test Author',
            title='Public Article',
            content='This is public content',
            preview='This is...',
            minutes_to_read=3,
            is_member_only=False
        )
        
        db.session.add_all([article1, article2])
        db.session.commit()
        
        yield
        
        db.session.remove()
        db.drop_all()