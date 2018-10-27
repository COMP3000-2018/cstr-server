# cstr-server 
Case Study Technology Revamp server side source code 
## Requirements 
  * Python 3.7     
    * Needs to be compiled with SSL suppoport if built from source 
  * [Flask](http://flask.pocoo.org/)
  * [Requests](http://docs.python-requests.org/en/master/) 
  * [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) if  deploying for production 
  * pip 
## Steps (develope environment) 
  1. Edit etc/hosts file if needed On Windows, this file is located at: 
  
  ```
  /etc/hosts/
  ```
  On Windows  
  ```
  c:\Windows\System32\Drivers\etc\hosts
  ``` 

  2. Set necessary environment variables:  
  * `FLASK_SECRET` needs to be cryptographically secure random string. This is used to create session cookies.  
  * `FLASK_APP` should be set to `cstr:create_app()`.  
  * `FASK_ENV` should be set to `development` if running in a dev environment. 

  3. Create a virtual environment, this should be in the root of the project. 
  ```
  $ cd cstr-server 
  $ python3.7 -m venv venv 
  ``` 
  4. Activate the virtual environment.

  5. Install the packages that this project depends on. 
    On macOS and Linux: 
  ``` 
  $ python setup.py install 
  ``` 
  6. Ensure that the current working directory is in the root of this project. 
  7. Start app by typing 
  ```
  $ flask run
  ```  
