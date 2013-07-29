import os
import cuenco
import unittest
import tempfile

class CuencoTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, cuenco.app.config['DATABASE'] = tempfile.mkstemp()
        cuenco.app.config['TESTING'] = True
        self.app = cuenco.app.test_client()
        cuenco.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cuenco.app.config['DATABASE'])
        
if __name__ == '__main__':
    unittest.main()