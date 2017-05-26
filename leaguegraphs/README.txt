To run the server, unzip file and in a command prompt inside this directory use the command:
python manage.py runserver

To flush the database run the command and enter "yes":
python manage.py flush

The locations of files are listed below:
HTML - loadprofile/templates/loadprofile
CSS & all PNG/JPG/SVG files - loadprofile/static/styles
JavaScript - loadprofile/static/scripts
Urls (urls.py) and Views (views.py) for page rendering and redirection - loadprofile
Database models - loadprofile/models.py
All API access handling and most database queries - loadprofile/util.py