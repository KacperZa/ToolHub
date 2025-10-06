from NASA_APOD import create_app, db
from Text_Analizer.routes import analyzer_bp
from NASA_APOD.routes import bp

app = create_app()
# app.register_blueprint(analyzer_bp, url_prefix='/analyzer')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# print (response.text)
