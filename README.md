# webapp
================================================================<br />

Test user <br />
login:      editor<br />
password:   editor<br />
================================================================<br />

Task:<br />
Create Pyramid web application using Python language.<br />
https://trypyramid.com/<br />
There are two types of users: editor and guests.<br />
Editor can login and create Articles.<br />
Article has next fields: date of publication, title, text, tags. Editor adds text of article using Rich Text Editor control.<br /> 
Tags - is the list of keywords separated by comma, these are added by Editor as well.<br />
Guests cannot login, but they can view articles, sort by date and filter them by tags.<br />
Also Guests can add comments.<br />
Please create application and deploy to Amazon AWS server, so it is accessible.<br />
Please use PostgreSQL as database.<br />

Review result:<br />
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
  
- Set and use a VENV environment variable
   
    export VENV=~/webapp

- Create a Python virtual environment, if not already created.

    python3 -m venv $VENV

- Upgrade packaging tools, if necessary.

    $VENV/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    $VENV/bin/pip install -e ".[testing]"

Before the next steps:
If you already have an old database, it is better to delete all tables from it.

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

        $VENV/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

        $VENV/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    $VENV/bin/initialize_webapp_db development.ini

- Run your project's tests.

   $VENV/bin/pytest -q

- Run your project.

    $VENV/bin/pserve development.ini --reload
