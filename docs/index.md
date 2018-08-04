![doc](https://img.shields.io/badge/coverage-9-red.svg)
![doc](https://img.shields.io/badge/test-pass-green.svg)
![doc](https://img.shields.io/badge/doc-available-blue.svg)
![doc](https://img.shields.io/badge/language-python-red.svg)


# envman 

`envman` is a small package exposing Python **and** REST APIs to manage 
commondata environments and platform parameters.




## Usage Primer

```python
# Parameter api

from envman  import Parameter 

# Puts a parameter related to an environment
Parameter.put_parameter(env="dev",name="VpcId", value="vpc-12345")


# Puts a parameter related to a platform
Parameter.put_parameter(env="dev",uri="uri:123456:platform:dev", name="PubSubnetId", value="subnet-12345")

# Gets a parameter
Parameter.get_parameter("dev","uri:123456:platform:dev", "PubSubnetId")
"subnet-12345"

# Gets all parameters as dict under an env
Parameter.get_parameters(env="dev")
{
    "Environment" : {
        "dev" : {
           "globals" : {
                "VpcId" : "vpc-12345"
            },
            "platforms" : {
                "uri:platform:123456:dev" : {
                    "PubSubnetId" : "subnet-12345"
                }
            }
            
        }
    }
}
# Gets all parameters as dict under a platform uri
Parameter.get_parameters(env="dev", uri="uri:platform:123456:dev" )
{
    "Environment" : {
        "dev" : {
            "platforms" : {
                "uri:platform:123456:dev" : {
                    "PubSubnetId" : "subnet-12345"
                }
            }
            
        }
    }
}
```






## Python Api 

**envman.Parameter.put_parameter**

- **env**(str) : environment key
- **uri**(str, optional) : resource uri
- **name**(str,optional) : name of the parameter
- **value**(str, optional) : value of the parameter
- **description**(string, optional) : description of the parameter

>    Creates a parameter in SSM under env  
     
    
    
**envman.Parameter.get_parameter**

- **env**(str) : environment key
- **uri**(str, optional) : resource uri
- **name**(str,optional) : name of the parameter

>   Reads  the parameter value in the given env.
>   One or both of uri and name must be provided
    
    
**envman.Parameter.get_parameters**

- **env**(str) : environment key
- **uri**(str, optional) : resource uri

>   Returns  a dict with all parameters under this env/uri
> The dict has following format : 
```python
{
"Environment" : {
    "<env>" : {
        "globals" : {
            "name" : "value"
        },
        "platforms" : {
            "<uri>" : {
                "name" : "value"
            }
        }
    
    }
    }
}
```



## REST Api 
**POST :/parameter**
- body.**env**(str)
- body.**uri**(str)
- body.**name**(str)
- body.**value**(str)
- body.**description**(string, *optional*

>    Creates a parameter in SSM with uri/resource_type/accountid/.../name 
    with the provided value  and description
    
    
**GET: /parameter**

- querystring.**env**(str)
- querystring.**uri**(str)
- querystring.**name**(str)

>   Reads  the parameter value
    
    
**GET :/parameters**

- querystring.**env**(str)
- querystring.**uri**(str)

>   Returns  a dict with all parameters under this env/uri


## REST API Programmatic Examples  with `requests`

```python
import requests
endpoint = "API GATEWAY endpoing"
# putting a parameter
response = requests.post(
    endpoint+"/parameter", 
    json = {
        "env" : "tests",
        "uri" :"uri:platform:123456:dev",
        "name" : "platformparam",
        "value": "platformvalue"
    }
)

# getting a parameter
response = requests.get(
    endpoint + "/parameter",
    params={
        "env" : "tests",
        "name": "platformparam",
        "uri": "uri:platform:123456:dev"
        }
)           


# getting all parameters in an environment 
response = requests.get(
    endpoint + "/parameters",
    params={
        "env" : "tests"
    }
)


```

## CLI usage

- Load configuration from local file into ParameterStore (under specific environment). If not specified, the *env* param will default to *dev* and the *filename* param will default to *config.json*

```sh
make load env=test filename=config.test.json 
```

- Show configuration from ParameterStore (under specific environment). If not specified, the *env* param will default to *dev*

```sh
make show env=test
```
