#!/usr/local/bin/python3
import os
from multiprocessing import Process
from time import process_time

os.environ['APP_ENV'] = 'development'

from app import app
import unittest
import tempfile
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def tearDown(self):
        pass
    def login(self, username, password):
        headers = [('Content-Type', 'application/json')]
        data = {'username': username, 'password': password}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        return self.app.post('/auth', headers=headers, data=json_data)
    def decode_token(self,inp):
        reqstr = str(inp.data,encoding='utf8')
        n = json.loads(reqstr)
        token = n['access_token']
        return token
    def post_request(self,token,url):
        headers = [('Content-Type', 'application/json'),
                  ('Authorization','JWT '+token)]
        return self.app.post(url, headers=headers)
    def get_request(self,token,url):
        headers = [('Content-Type', 'application/json'),
                  ('Authorization','JWT '+token)]
        return self.app.get(url, headers=headers)
    def delete_request(self,token,url):
        headers = [('Content-Type', 'application/json'),
                  ('Authorization','JWT '+token)]
        return self.app.delete(url, headers=headers)

    # ===================================================== #
    # ====                                             ==== #
    # ==== all the methods with test_ in begin - tests ==== #
    # ====                                             ==== #
    # ===================================================== #

    # ==== Test 1 ==== #
    def test_1_server(self):
        # test that index.html is available
        rv = self.app.get('/')
        assert 'URL' in str(rv.data,encoding='utf8'),\
          'index.html for minirest app is not available'

    # ==== Test 2 ====
    # test login process
    def test_2_login_super(self):
        rv = self.login('cisco', 'cisco')
        assert 'token' in str(rv.data,encoding='utf8'),\
            'cant login to api and receive token with correct credentials'
        token = self.decode_token(rv)
        # now we should check this token
        rv = self.get_request(token,'/api/auth/test')
        assert 'ok' in str(rv.data,encoding='utf8'),\
            'no authentication test ok found'

    # ==== Test 3 ====
    # test api login process
    def test_3_login_logout(self):
        # test for right username/password
        rv = self.login('cisco', 'cisco')
        #print(str(rv.data,encoding='utf8'))
        assert 'token' in str(rv.data,encoding='utf8'),\
            'cant login to api and receive token with correct credentials'
        # test for wrong username
        rv = self.login('adminx', 'cisco')
        #print(str(rv.data,encoding='utf8'))
        assert 'Invalid' in str(rv.data,encoding='utf8'),\
           'test for wrong username failed'
        # test for wrong password
        rv = self.login('cisco', 'isco')
        #print(str(rv.data,encoding='utf8'))
        assert 'Invalid' in str(rv.data,encoding='utf8'),\
            'wrong password test failed'

    # ==== Test 4 ====
    # start L_THUMB for 10 periods
    def test_4_thumb_start(self):
        rv = self.login('cisco', 'cisco')
        assert 'token' in str(rv.data,encoding='utf8'),\
            'cant login to api and receive token with correct credentials'
        token = self.decode_token(rv)
        # now we should check this token
        rv = self.post_request(token,'/api/v1/start/L_THUMB/1/10')
        assert 'ok' in str(rv.data,encoding='utf8'),\
            'no test ok found'

    # ==== Test 5 ====
    # start R_THUMB for 10 periods
    def test_5_thumb_start(self):
        rv = self.login('cisco', 'cisco')
        assert 'token' in str(rv.data,encoding='utf8'),\
            'cant login to api and receive token with correct credentials'
        token = self.decode_token(rv)
        # now we should check this token
        rv = self.post_request(token,'/api/v1/start/R_THUMB/1/10')
        assert 'ok' in str(rv.data,encoding='utf8'),\
            'no test ok found'

    # ==== Test 6 ====
    # stop R_THUMB
    def test_6_thumb_stop(self):
        rv = self.login('cisco', 'cisco')
        assert 'token' in str(rv.data,encoding='utf8'),\
            'cant login to api and receive token with correct credentials'
        token = self.decode_token(rv)
        # now we should check this token
        rv = self.post_request(token,'/api/v1/stop/R_THUMB')
        assert 'ok' in str(rv.data,encoding='utf8'),\
            'no test ok found'

if __name__ == '__main__':
    unittest.main()
