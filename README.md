# Shelter Prototype

## About the Prototype
Hello! Thanks for reviewing this code.
This project makes use of Flask, SQLLite and Bootstrap. 
I decided to try out Flask, a framework I had never developed with before. I hope this demonstrates my ability to learn and contribute to a project quickly.

I used code from [Miguel Grinberg's Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination) and ChatGPT as references.
I focused on the APIs and database, leaving the styling to minimal Bootstrap CSS.


### Future Improvements:
- Ability to build an offline report PDF (with a message queue and workers)
- Caching
- Tests
- Complete UI and styling (including better verification of inputs)
- Pagination on online reports
- User registration and management
- Docker

## Running the code
```shell
# install python3 and clone repository
# create python virtual env
python3 -m venv venv
# activate environment
source venv/bin/activate
#install requirements (make sure you're in base directoyr of repo)
pip install -r requirements.txt
#should work without but just in case
export FLASK_APP=app.py
#run flask
flask run
#view http://127.0.0.1:5000/ in browser
#login with admin/admin
