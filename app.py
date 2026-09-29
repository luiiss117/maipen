from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=False)

# Uncomment this line and comment the one above to enable ssl
#    app.run(host="127.0.0.1",port=5000,debug=False, ssl_context=('certs/web-maipen.crt', 'certs/private/web-maipen.key'))
