from friend import app
import unittest


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        # Wrong key:
        # app.config['CSRF_ENABLED'] = False
        # Right key:
        app.config['WTF_CSRF_ENABLED'] = False

    # Ensure Sign in, behaves correctly 
    def test_account_signup(self):
        tester = app.test_client(self)
        tester.post('/signup', data=dict(firstname="test",lastname="test",email="test@test.com",password="password"),
                follow_redirects = True
                )
        response = tester.get('/profile', follow_redirects=True)
        self.assertIn(b'Welcome test@test.com\'s profile page', response.data)


    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signin', content_type='html/text')
        self.assertTrue(b'Sign In' in response.data)

    # Ensure login behaves correctly give the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
                '/signin',
                data=dict(email="test@test.com", password="password"),
                follow_redirects = True)
        self.assertIn(b'Welcome test@test.com\'s profile page', response.data)


    # Ensure login behaves correctly give the in incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
                '/signin',
                data=dict(email="test@test.com", password="wrong"),
                follow_redirects = True
                )
        self.assertIn(b'Invalid e-mail or password', response.data)

    # Ensure logout behaves correctly give the correct credentials
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
                '/signin',
                data=dict(email="test@test.com", password="password"),
                follow_redirects = True
                )
        response = tester.get('/signout', follow_redirects=True)
        self.assertIn(b'Welcome to APP', response.data)

    # Ensure that the main page require login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/profile', follow_redirects=True)
        self.assertTrue(b'Sign In' in response.data)


    # Ensure Adding new friend, behaves correctly give the correct credentials
    def test_add_friend(self):
        tester = app.test_client(self)
        tester.post(
                '/signin',
                data=dict(email="test@test.com", password="password"),
                follow_redirects = True
                )
        tester.post('/friends', data=dict(f_firstname="test",f_lastname="test",f_email="test@test.com",f_phone="1234567890"),
                follow_redirects = True
                )
        response = tester.get('/showall', follow_redirects=True)
        self.assertIn(b'1234567890', response.data)


    # Ensure Adding new friend, behaves correctly give the correct credentials
    def test_contact(self):
        tester = app.test_client(self)
        response = tester.post('/contact', data=dict(name="test",email="test@test.com",subject="test",message="Test Hello"),
                follow_redirects = True
                )
        #response = tester.get('/contact', follow_redirects=True)
        self.assertIn(b'Thank you for your message. We\'ll get back to you shortly.', response.data)


    # Ensure Deleting Account, behaves correctly
    def test_zero_delete_account(self):
        tester = app.test_client(self)
        tester.post(
                '/signin',
                data=dict(email="test@test.com", password="password"),
                follow_redirects = True
                )
        response = tester.get('/delete', follow_redirects=True)
        self.assertIn(b'Welcome to APP', response.data)

if __name__ == '__main__':
    unittest.main()
