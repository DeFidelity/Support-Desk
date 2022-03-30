# Support-Desk
In organization customer support desk.

## Installation 
- Run `git clone https://github.com/DeFidelity/Support-Desk` 
- Install dependencies by running `pip install -r requirents.txt` in a virtual environment

### Testing permissions and entire code base automatically [Unit testing]

- To test this project, especially in the aspect of permissions and validations, its not neccesary to run the project because i have already written test inside the project that test for bruises from all the views, urls and forms, just navigate into the poject directory, the same level with manage.py and run `python manage.py test` this command would run through all already configured tests and check for prescribed permissions, check `supportdesk/tests` for all tests and configurations.

### Manual testing and UX check 

- Run `python manage.py runserver` to access the whole project on `localhost:8000`

#### Kindly note 

`db.sqlite3` was committed together with the code so that you would not need to write any tickets before testing the project if only you log in as staff.
