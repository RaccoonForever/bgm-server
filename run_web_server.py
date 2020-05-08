# pylint: disable=line-too-long
"""
Main script to run the server
"""
from main import create_app

app = create_app()

if __name__ == "__main__":
    print "* Starting web service ... \n please wait until server has fully started *"
    app.run(host=app.config['FLASK_RUN_HOST'], port=app.config['FLASK_RUN_PORT'])
