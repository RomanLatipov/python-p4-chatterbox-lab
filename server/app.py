from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)



@app.get('/messages')
def get_rqst():
    messages = [msg.to_dict() for msg in Message.query.order_by(Message.created_at).all()]
    return messages, 200

@app.post('/messages')
def post_rqst():
    message = Message(body=request.json['body'], username=request.json['username'])
    db.session.add(message)
    db.session.commit()
    return message.to_dict(), 201

@app.patch('/messages/<int:id>')
def patch_rqst(id):
    message = Message.query.where(Message.id == id).first()
    if message:
        for key in request.json.keys():
            if not key =='id':
                setattr(message, key, request.json[key])

        db.session.add(message)
        db.session.commit()

        return message.to_dict(), 202
    
    else:
        return {"error": "Not found"}, 404
    
@app.delete('/messages/<int:id>')
def delete_rqst(id):
    message = Message.query.where(Message.id == id).first()
    if message:
        db.session.delete(message)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "Not found"}, 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
