import sys
sys.path.insert(0, './application.py')  # Replace '/path/to/your/flask/app' with the actual path to your Flask app

from application import app  # Replace 'your_flask_app' with the name of your Flask app object

application = app 







I'm deploying my flask server on pythonanywhere.com , 
in the Web page , Code area : 
i have : 
 - Source code : /home/elouazzaniaymane/mysite , under mysite 
	i have two file , application.py which is the file for
	my flask app , and key.json contains some info about 
	firebase 
 - in the wsgi configuration file , i have 
	import sys

	project_home = u'/home/elouazzaniaymane/mysite'
	if project_home not in sys.path:
    	sys.path = [project_home] + sys.path


	from application import app as application

once i launch the web app , i get this error : 
Error running WSGI application
2023-05-21 11:27:59,428: ModuleNotFoundError: No module named 'application'
2023-05-21 11:27:59,428:   File "/var/www/elouazzaniaymane_pythonanywhere_com_wsgi.py", line 5, in <module>
2023-05-21 11:27:59,429:     from application import app
	





