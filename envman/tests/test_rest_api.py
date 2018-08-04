import requests
import unittest
import boto3
from envman import Parameter
import pprint

class TestRestApi(unittest.TestCase) :
    @classmethod
    def setUpClass(cls):
        cls.endpoint= "https://9sji3igg24.execute-api.eu-west-1.amazonaws.com/prod"
        Parameter.clean_environment(env="tests")



    def test_parameter_api(self):
        endpoint = TestRestApi.endpoint
        response = requests.post(endpoint+"/parameter", json = {
            "env" : "tests",
            "uri" :"uri:platform:123456:dev",
            "name" : "platformparam",
            "value": "platformvalue"})

        response = requests.post(endpoint+"/parameter",json = {
            "env": "tests",
            "name": "globalparam",
            "value": "globalvalue"
        })

        print response

        self.assertEqual(response.json()["success"] , True)
        response = requests.get(endpoint + "/parameter",
                                 params={"env" : "tests",
                                       "name": "platformparam",
                                       "uri": "uri:platform:123456:dev"
                                       })

        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["data"], "platformvalue")

        response = requests.get(endpoint + "/parameters",params={"env" : "tests"})
        print response.json()
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["data"]["Parameters"]["tests"]["uri:platform:123456:dev"]["platformparam"], "platformvalue")




