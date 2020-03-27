# Flask Architecture 1.3


This project contains the template/boilerplate code for running Flask applications in PCF. Use this to kickstart your new projects!

# Features

This project will provide you these features with minimal configuration required.
  - SSO
  - Unit Testing 
  - Database Migrations
  - Logging
  - Python/Flask best practices: Blueprints, Factories, PyLint, etc.
  - AngularJS + Angular Animations
  - Bootstrap4
  - Caching solution for static files
  - CI/CD pipeline, with Fortify security code scans, SonarQube quality code scans and automated deployments to PCF

# Getting started

Install Python https://www.python.org/
Download the code in this repository.
Run setup_app.ps1 and provide your application name.
Import the files on your favorite IDE and you're all set! 


# Creating Blueprints

Use Flask Blueprints to add resources to your REST Api. To create a Blueprint create a sub-folder with the resources name, then create a file called __views.py__  with your Blueprint routes. For example, when creating a Blueprint for employee data, this would be __app\employee\views.py__: 
```python
from flask import Blueprint, jsonify, make_response, request
import app.database as db
from .models import Employee

employee_bp = Blueprint('employee', __name__, url_prefix='/api/employee')

@employee_bp.route('/', methods=['GET'])
def employee_get():
    badge = request.args.get('badge')
    employee = Employee.get_employee_by_badge(badge)
    if employee is None:
        return make_response('', 204)
    return jsonify({
        "badge": employee.badge,
        "nt_logon": employee.nt_logon,
        "manager_badge": employee.manager_badge,
        "email": employee.email,
        "name": employee.name,
        "updated_at": employee.updated_at
    })
```

Now on __app.py__ use the *_register_blueprints* function to register your Blueprints with the application. For example:

```python
def _register_blueprints(application):
    '''Register blueprints with our application'''
    from app.login import login_bp
    from app.frontend import frontend_bp
    from app.employee import employee_bp
    application.register_blueprint(login_bp)
    application.register_blueprint(frontend_bp)
    application.register_blueprint(employee_bp)
```

# Using Database Migrations

On your Blueprints define your models in __models.py__. Here's a sample model, __app\employee\models.py__:
```python
from sqlalchemy import Column, String, DateTime
from app.database import Base
from app.utils import get_current_time

class Employee(Base):
    '''Model class for employee table'''
    __tablename__ = 'employee'

    badge = Column(String(21), primary_key=True)
    nt_logon = Column(String(100))
    manager_badge = Column(String(21))
    email = Column(String(100))
    name = Column(String(100))
    updated_at = Column(DateTime(), default=get_current_time)
```
On __database.py__ import all your models on the _get_metadata_ function. Then add their metadata to the return array. For example:
```python
def get_metadata():
    '''Import all modules that define models here!
      Otherwise alembic won't be able to detect database changes automatically'''
    from app.employee.models import Employee
    return [Employee.metadata]
```
On cmd run this command: 
                        
    alembic revision --autogenerate -m "commit_name"

Review the generated py file at ./alembic/versions, make any required changes. When running this code on a new database alembic will upgrade the database to the latest version!

# Running Unit Tests

On your Blueprints define your tests in __tests.py__. To test the Employee Blueprint we created on the previous sections, this would be __app\employee\tests.py__:
```python
from unittest import TestCase
from app.app import create_app
from app.config import AppTestConfig

class EmployeeTest(TestCase):
    '''Tests for employee module'''

    def setUp(self):
        self.app = create_app(AppTestConfig())

    def test_all_employees_not_empty(self):
        ''' Should return an employee array '''
        self.test_create_employee()
        with self.app.test_client() as client:
            resp = client.get('/api/employee/')
            data = json.loads(resp.data)
            assert data.get('employees')
```
Then import all your tests in the main tests.py file in the Api folder. For example:
```python
from unittest import main
from app.employee.tests import EmployeeTest

if __name__ == '__main__':
    main(verbosity=2)
```
Finally, to run the tests and coverage report use these commands on cmd:

    coverage run --source app tests.py
    coverage report

# Frontend

Your Frontend is a Single-Page Application (SPA). That means all frontend content is static, so include it on __app\frontend\static__ and it will be automatically be picked up by the included Frontend blueprint. 

If you do not wish a Frontend you may remove the Frontend folder and the Blueprint from __app\app.py__

__Controlling cache__ 

Caching can sometimes cause issues, whenever deploying new versions of javascript/html files make sure to include a version parameter to make sure browser refresh their cached versions of said file. For example, say you deploy this app.js on your first go-live:
```javascript
<script type="text/javascript" src="./app.js"></script>
```

Then on your second deployment you can add ?v=2. That will cause browsers to ignore the old cached version and use the new one:
```javascript
<script type="text/javascript" src="./app.js?v=2"></script>
```
By default your index.html will not be cached. 

# Logging

When running on PCF we're using logging level warning by default. You can change that by changing the PCF loglevel environment variable. Strongly recommend not using a logging level higher than warning.

To use the logging correctly __do not use print()__, instead use Flask's logger object:
```python
from flask import current_app

current_app.logger.debug('shows on log level debug only')
current_app.logger.info('shows on log level info or lower')
current_app.logger.warning('shows on log level warning or lower')
current_app.logger.error('shows on log level error or lower')
current_app.logger.critical('always shows')
```


