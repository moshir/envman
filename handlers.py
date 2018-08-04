import pprint
import json
from datetime import datetime, date
from envman.api import App

app = App.get()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return str(obj)


def handler(event, context):
    print "* "*30
    print "Query = "
    print pprint.pformat(event [u'queryStringParameters'])

    print "Body ="
    print pprint.pformat(event [u'body'])
    baseresponse = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    }
    try:
        data = app.route(event)
        baseresponse["body"] = {"success": True, "data": app.route(event)}
    except Exception, e:
        print "=>", e
        baseresponse["body"] = {
            "success": False,
            "error": "Unexpected Errors"
        }
    baseresponse["body"] = json.dumps(baseresponse["body"], default=json_serial)
    return baseresponse


if __name__ == "__main__":
    events  =[]
    events.append(  {u'body': u'{"env" : "dev", "value" : "", "name": "VpcId", "uri": "uri:account:123456"}',
             u'httpMethod': u'POST',
             u'path': u'/parameter/put_parameter'
             }
    )


    events.append(  {u'body': u'{"env" : "dev", "value" : "subnet1234", "name": "publicSubnetId", "uri": "uri:account:123456"}',
             u'httpMethod': u'POST',
             u'path': u'/parameter/put_parameter'
             }
    )

    events.append(  {u'body': u'{"env" : "dev"}',
             u'httpMethod': u'POST',
             u'path': u'/parameter/get_parameters'
             }
    )
    for event in events:
        print handler(event, {})
