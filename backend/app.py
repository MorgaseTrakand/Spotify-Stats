from flask import Flask
from flask_restx import Api
from auth2 import auth_ns
from flask_cors import CORS

def create_app(config):
  app=Flask(__name__)
  app.config.from_object(config)

  
  CORS(app, supports_credentials=True)

  #flask_restx initialization
  api=Api(app, doc='/docs')
  
  #namespaces
  api.add_namespace(auth_ns)
  
  return app
