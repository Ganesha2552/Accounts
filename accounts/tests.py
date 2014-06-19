"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
import urllib2

'''
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
'''
        
accounts_url="http://tzu-lin02.tsi.zohocorpin.com:8002/accounts/emailapi/"
    
def getSession(url):
    try:
        req=urllib2.Request(url)
        resp=urllib2.urlopen(req)
        resp_str=resp.read()
        return resp_str
    except Exception as e:
        return e
        
def test():
    url=accounts_url+"?"
    url=url+"list=mei"
    print getSession(url)
    
test()
