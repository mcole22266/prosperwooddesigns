# wsgi.py
# Michael Cole
#
# Execution of create_app following App Factory Pattern
# -----------------------------------------------------

from .prosperwooddesigns import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
