import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
import mysql.connector as msql
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from mysql.connector import Error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:finale-95V@127.0.0.1: 3306 /manga_project'
db = SQLAlchemy(app)

###Models####
class Mangas(db.Model):
    __tablename__ = "class_mangas"
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50))
    style = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    synopsis = db.Column(db.String(500))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, titre, style, genre, synopsis):
        self.titre = titre
        self.style = style
        self.genre = genre
        self.synopsis = synopsis

    def __repr__(self):
        return '' % self.id

db.create_all()

api = Api(app)
try:
    config = {
      'user': 'root',
      'password': 'finale-95V',
      'host': '127.0.0.1',
      'database': 'manga_project',
      'raise_on_warnings': True
    }

    df = pd.read_csv('C:/Users/diogo/OneDrive/Documents/Ynov/B3/python/projet_final/adn.csv', sep=',', header=1)
    conn = msql.connect(**config)
    if conn.is_connected():
        cursor = conn.cursor()

        for i, row in df.iterrows():
            sql = "INSERT INTO manga_project.class_mangas VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

class Manga(Resource):
    def get(self):
        cursor = conn.cursor()
        query = "select * from manga_project.class_mangas"
        cursor.execute(query)
        mangas = cursor.fetchall()
        print(mangas)
        cursor.close()
        return {'mangas': mangas}
api.add_resource(Manga, '/mangas')

class MangasSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Mangas
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    titre = fields.String(required=True)
    style = fields.String(required=True)
    genre = fields.String(required=True)
    synopsis = fields.String(required=True)

@app.route('/mangas/<id>', methods=['GET'])
def get_mangas_by_id(id):
    get_mangas = Mangas.query.get(id)
    mangas_schema = MangasSchema()
    mangas = mangas_schema.dump(get_mangas)
    return make_response(jsonify({"mangas": mangas}))

@app.route('/mangas/<id>', methods=['PUT'])
def update_mangas_by_id(id):
    data = request.get_json()
    get_mangas = Mangas.query.get(id)
    if data.get('titre'):
        get_mangas.titre = data['titre']
    if data.get('style'):
        get_mangas.style = data['style']
    if data.get('genre'):
        get_mangas.genre = data['genre']
    if data.get('synopsis'):
        get_mangas.synopsis = data['synopsis']
    db.session.add(get_mangas)
    db.session.commit()
    mangas_schema = MangasSchema(only=['id', 'titre', 'style', 'genre', 'synopsis'])
    mangas = mangas_schema.dump(get_mangas)
    return make_response(jsonify({"mangas": mangas}))

@app.route('/mangas/<id>', methods=['DELETE'])
def delete_mangas_by_id(id):
    get_mangas = Mangas.query.get(id)
    db.session.delete(get_mangas)
    db.session.commit()
    return make_response("", 204)

@app.route('/mangas', methods=['POST'])
def create_mangas():
    data = request.get_json()
    mangas_schema = MangasSchema()
    mangas = mangas_schema.load(data)
    result = mangas_schema.dump(mangas.create())
    return make_response(jsonify({"mangas": result}), 200)

if __name__ == "__main__":
    app.run(debug=True)