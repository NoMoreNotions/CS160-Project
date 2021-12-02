from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    #First run to ensure flask was setup correctly
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type = 'html/text')
        self.assertEqual(response.status_code, 200)

    #Ensure that the login page loads correctly
    def test_login_page_loads(self):
            tester = app.test_client(self)
            response = tester.get('/login', content_type = 'html/text')
            self.assertTrue(b'Log In' in response.data)

    #Ensure that the login behaves correctly with correct credentials
    def test_login_correct(client, email, password):
        return client.post('/login', data=dict(
            email = 'david.troung@sjsu.edu',
            password = 'password'
        ), follow_redirects=True)
        self.assertTrue(b'Welcome, David Truong!' in response.data)

    #Ensure that the login behaves correctly with incorrect credentials
    def test_login_incorrect(self):
            tester = app.test_client(self)
            response = tester.post('/login', 
            data=dict(email = 'random@gmail', password = 'password'), 
                    follow_redirects = True)
            self.assertTrue(b'Please check your login details and try again.' in response.data)

    #Ensure that the logout behaves correctly
    def logout(client):
        return client.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()