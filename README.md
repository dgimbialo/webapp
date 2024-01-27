# webapp
================================================================

#Test user
#Login:      editor
#Password:   editor
================================================================

Task:
Create Pyramid web application using Python language.
https://trypyramid.com/
There are two types of users: editor and guests.
Editor can login and create Articles. 
Article has next fields: date of publication, title, text, tags. Editor adds text of article using Rich Text Editor control. 
Tags - is the list of keywords separated by comma, these are added by Editor as well.
Guests cannot login, but they can view articles, sort by date and filter them by tags. 
Also Guests can add comments.
Please create application and deploy to Amazon AWS server, so it is accessible. 
Please use PostgreSQL as database.

Review result:
1. Task is done except one requirement: "guests can sort by date". I would improve many things in this task, but next you can find some of the recommendations.
2. I would implement tags with links.
3. Comments I would sort time descending.
4. Improve displaying the list of the articles to users.

Technical.
1. Technically task is done well. Besides a few recommendations below.
2. Remove all binary file from git. It should be only source code, use .gitignore.
3. Move JavaScript from .jinja2 into .js file.

================================================================

Getting Started
---------------
- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py.

    cd webapp

- Create a Python virtual environment, if not already created.

    python3 -m venv env

- Upgrade packaging tools, if necessary.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

        env/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

        env/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    env/bin/initialize_webapp_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
