import boto3
from gotolambda import Config, Builder
import os

class Deploy:
    @classmethod
    def run(cls):
        cls.session = boto3.session.Session(region_name="eu-west-1")
        cls.conf = Config(
            venv=False,
            distfolder="/tmp/builds",
            srcfolder = os.path.join(os.path.dirname(os.path.dirname(__file__)),"envman"),
            bucket="edp.bucket",
            objectkey="envman.zip",
            session=cls.session,
            function_name="envman"
        )
        print cls.conf
        builder = Builder(cls.conf)
        builder.build()


if __name__== "__main__" :
    Deploy.run()