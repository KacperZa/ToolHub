from NASA_APOD import create_app, db
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# print (response.text)
