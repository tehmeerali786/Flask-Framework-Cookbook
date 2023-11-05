from flask import Flask 
app = Flask(__name__)
@app.route('/')
@app.route('/hello')
@app.route('/hello/<user>')
def hello_world(user=None):
    user = user or 'Shalabh'
    return '''

            <html>
            
                <head>
                        <body>
                                <h1>Hello %s!</h1>
                                <p>Welcome to the World of Flask!</p>
                        </body>
                </head>
            </html>
            ''' % user 
            


if __name__ == '__main__':
    app.run()