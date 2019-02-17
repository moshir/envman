import boto3
from urilib import Uri
import pprint
import json
from retrying import retry
from botocore.exceptions import ClientError
import logging

log = logging.getLogger("envman:Parameter")

class Parameter:
    cache={}
    @classmethod
    def ssm(cls):
        client =  boto3.client("ssm", region_name="eu-west-1")
        return client

    @classmethod
    def get_parameter_name(cls, env, uri, name=""):
        adapturi = uri.replace(":", "/")
        pname = "/commondata/%(env)s/%(adapturi)s/%(name)s"%vars() if len(name) else "/commondata/%(env)s/%(adapturi)s"%vars()
        clean = pname.replace("//","/")
        return clean

    @classmethod
    def parse_parameter_name(cls, parametername):
        parts = parametername.split("/")
        env = parts[2]
        uri = parts[3]
        if uri == "uri" :
            #uri:platform:123456:dev
            uristring = ":".join(parts[3:7])
            #Uri.parse(uristring)
            return {
                "type" : "platform",
                "env" : env,
                "uri" : uristring,
                "name" : "/".join(parts[7:])
            }
        else :
            return {
                "type": "env",
                "env": env,
                "name": "/".join(parts[3:])
            }

    @classmethod
    def put_parameter(cls, env, uri="", name="", value="", description = None):
        pname =cls.get_parameter_name(env, uri, name)
        ssm = cls.ssm()
        response = ssm.put_parameter(
            Name=pname,
            Description=str(description),
            Value=str(value) if len(str(value)) else "-",
            Type='String' ,
            Overwrite=True
        )
        #return response
        return Parameter.get_parameter(env,uri,name)


    @classmethod
    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_parameter(cls, env, uri="", name=""):
        pname = cls.get_parameter_name(env,uri, name)
        if pname in cls.cache.keys():
            return Parameter.cache[pname]
        ssm = cls.ssm()
        try :
            param_value = ssm.get_parameter(
                Name = pname
            )["Parameter"]["Value"]
            cls.cache[pname] = param_value
            return param_value
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                log.warning("Parameter `{}` not found for env `{}`, defaulting to None".format(name, env))
                return None
            else:
                log.error("Error trying to retrieve parameter from SSM")
                raise e

    @classmethod
    def clean_environment(cls, env, uri=""):
        params = cls.get_parameters(env=env, uri=uri, flat=True)
        for p in params.keys() :
            pname= Parameter.get_parameter_name(env=env, uri="", name=p)
            cls.ssm().delete_parameter(Name = pname )


    @classmethod
    def get_parameters(cls, env, uri="",flat= False):
        response = {"Parameters" : {
            env : {
                "globals" : {

                }

            }
        }}
        pname = cls.get_parameter_name(env,uri,"")
        ssm = cls.ssm()
        try:
            paginator = ssm.get_paginator('get_parameters_by_path')
            operation_parameters = {'Path': pname, 'Recursive': True}
            page_iterator = paginator.paginate(**operation_parameters)
            for page in page_iterator:
                parameters = page['Parameters']
                if flat is True:
                    return {p["Name"].replace(pname,"") :p ["Value"] for p in parameters}
                for p in parameters :
                    parse = cls.parse_parameter_name(p["Name"])
                    if parse["type"] == "env" :
                        response["Parameters"][env]["globals"][parse["name"]] = p["Value"]
                    else:
                        if parse["uri"] not in response["Parameters"][env].keys():
                            response["Parameters"][env][parse["uri"]] = {}
                        response["Parameters"][env][parse["uri"]][parse["name"]] = p["Value"]
            return response
        except Exception, e:
            return response



    @staticmethod
    def show( env, uri=""):
        response = Parameter.get_parameters(env, uri)
        Parameter.printTree(response)

    @staticmethod
    def printTree(tree, depth=0):
        if tree == None or len(tree) == 0:
            print ".." * depth, " (empty)"
        else:
            if type(tree) == type({"a" : "dict"}):
                for key, val in tree.items():
                    if (type(val)==type({"a":"dict"})):
                        print ".." * depth, key
                        Parameter.printTree(val, depth + 1)
                    else :
                        print ".."*depth,key,":", val
            else :
                print ".." * depth, str(tree)



    @classmethod
    def load(cls, filename, env="dev"):
        try :
            f = open(filename)
        except Exception, e :
            raise Exception("Could not load", filename)

        body = "\n".join(f.readlines())
        config = json.loads(body)

        total = sum([len(config[topic]) for topic in config.keys()])
        done = 1
        print "Writing %(total)s `global` parameters in %(env)s Environment"%vars()
        for topic in config.keys() :
            for param in config[topic].keys() :
                print "     %(done)s/%(total)s written"%vars()
                Parameter.put_parameter(env=env, name="/".join([topic,param]),value = config[topic][param])
                done+=1

    @classmethod
    def __load(cls, filename, env=None, uri=None):
        try :
            f = open(filename)
        except Exception, e :
            raise Exception("Could not load", filename)

        body = "\n".join(f.readlines())
        config = json.loads(body)
        if env is None :
            for envname in config.keys() :
                for parameter in config[envname].keys() :
                    Parameter.put_parameter(env=envname, name=parameter, value=config[envname][parameter])

        else :
            if uri is None :
                for parameter in config.keys() :
                    Parameter.put_parameter(env=env, name=parameter, value=config[parameter])
            else :
                for parameter in config.keys() :
                    Parameter.put_parameter(env=env, name=parameter, uri=uri, value=config[parameter])



