import requests
import unittest
import boto3
from envman import Parameter
class TestPyApi(unittest.TestCase) :

    def test_afirst_clean_environment(self):
        Parameter.clean_environment(env="tests")
        params =Parameter.get_parameters(env="tests")
        self.assertEqual(len(params["Parameters"]["tests"]["globals"].keys()), 0)
        Parameter.show(env="tests")



    def test_env_parameter(self):
        Parameter.put_parameter(env= "tests", name = "AWSAccountId",value="123456789012")
        p = Parameter.get_parameter(env="tests", name="AWSAccountId")
        self.assertEqual(p, "123456789012")
        Parameter.show(env="tests")



    def test_platform_parameter(self):
        Parameter.put_parameter(env= "tests", uri="uri:platform:123456:dev", name = "AWSAccountId",value="123456789012")
        p = Parameter.get_parameter(env="tests", uri="uri:platform:123456:dev",name="AWSAccountId")
        self.assertEqual(p, "123456789012")
        Parameter.show(env="tests")

    def test_zlast_list_parameters(self):
        x  = Parameter.get_parameters(env="tests")
        envparams = x["Parameters"]["tests"]["globals"]
        platformparams = x["Parameters"]["tests"]["uri:platform:123456:dev"]


        self.assertEqual(len(envparams.keys()),1)
        self.assertEqual(len(platformparams.keys()),1)

        Parameter.show(env="tests")









