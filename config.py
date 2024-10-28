import os
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://admin:O9TXTq5c31xclcOhBob1mDrPqyn4dvU5@dpg-csfsnktsvqrc739r60kg-a/axolotl_ya4x")
SQLALCHEMY_TRACK_MODIFICATIONS = False
