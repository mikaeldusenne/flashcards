from flask import Flask, render_template, jsonify, redirect, flash, request, url_for, Response, Blueprint
import flask
from flask_caching import Cache
import logging
import random
from bson import ObjectId
import json
import numpy as np
import pandas as pd
import traceback
from datetime import datetime
from pprint import pprint
from os import environ
import os

from backend.src.pytypes import conv, Card, CardLang, V
import backend.src.helpers as h
import backend.src.db as db

cache = Cache(config={
    # 'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': '/.flask-cache', "CACHE_DEFAULT_TIMEOUT": 9999999
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://redis',
    'CACHE_REDIS_PORT': '6379',
    "CACHE_DEFAULT_TIMEOUT": 9999999,
})


def logging_setup(path):
    loggingdest = os.path.join(path, "flask.log")
    print("setting logging to {}".format(loggingdest))

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    # format='%(asctime)s\t%(name)s\t%(funcName)s\t%(levelname)s\t%(message)s'
    rootLogger = logging.getLogger('mikarezoo-flashcards')
    rootLogger.setLevel(logging.DEBUG if os.environ.get(
        "PROD", False) else logging.WARNING)

    fileHandler = logging.FileHandler(loggingdest)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)


logging_setup(".")


flsk = Blueprint(
    'bprnt', __name__,
    static_folder='./backend/static',
)

@flsk.route("/status", methods=["GET"])
def health_check():
    logging.debug("debug log")
    logging.info("info log")
    logging.warning("warning log")
    logging.error("error log")
    # logging.exception("exception log")
    return make_response("OK", 200)


@flsk.route("/api/cards", methods=["GET"])
def get_cards():
    # cards = [Card([CardLang("fr", "test")])]
    
    args = {}
    if "search" in request.args and request.args['search'] is not None and len(request.args['search']):
        args['langs'] = {'$elemMatch': {"text": {"$regex": h.prepare_user_input_search_regex(request.args['search'])}}}
    cards = db.db.cards.find(args)
    
    total_n = db.db.cards.count_documents(args)
    
    if "offset" in request.args:
        cards = cards.skip(int(request.args["offset"]))
        
    if "first" in request.args:
        cards = cards.limit(int(request.args["first"]))
    
    # logging.exception("exception log")
    return jsonify(dict(n=total_n, cards=[V.decode(e).toDict() for e in cards]))


@flsk.route("/api/update-usercard", methods=["POST"])
def update_usercard():
    user = request.json['user']
    card = ObjectId(request.json['card'])
    difficulty = request.json['difficulty']
    print("update user card", request.json)
    already = db.db.usercards.find_one({'user': user, "card": card})

    bucket = 0 if already is None else already['bucket']
    BUCKET_MAX = 2

    card_id = ObjectId(card)
    
    diffbk = dict(
        easy=1,
        normal=0,
        hard=-1
    )
    new_bucket = max(0, min(BUCKET_MAX, bucket+diffbk[difficulty]))
    
    reviewed = datetime.now()
    if already is None:
        db.db.usercards.insert({
            'user': user,
            "card": card_id,
            "bucket": new_bucket,
            "reviewed": reviewed,
        })
    else:
        db.db.usercards.update_one(
            {'user': user, "card": card_id},
            {"$set": {"bucket": new_bucket, "reviewed": reviewed}}
        )
    # print("CARD", card)
    
    print(f"Update Bucket {bucket} -> {new_bucket}: {describe_card(card)}")
    return jsonify(dict(bucket=new_bucket))

def describe_card(card_id):
    return " / ".join([e['text'] for e in db.db.cards.find_one({'_id': ObjectId(str(card_id))})['langs']])

def _train_cards(user):
    # db.db.usercards.find({user: user}, {'_id': 0})
    # from bson import ObjectId
    # db.db.usercards.find_one({'user': 'mika', "card": ObjectId('6147176f65625f5c941084dd')})

    # user = "mika"
    usercards = list(db.db.usercards.aggregate([
        {'$match': {"user": user}},
        {"$lookup": {
            "localField": "card",
            "foreignField": "_id",
            "from": "cards",
            "as": "card"
        }},
        {"$unwind": "$card"},
        {'$project': {"_id": 0}},
    ]))
    
    # usercards
    
    def prepare_user_card(e):
        e["card"] = V.decode(e['card']).toDict()
        return e
    
    usercards = {e["card"]['id']: e for e in map(prepare_user_card, usercards)}
    
    # usercards
    # cards = {c.id: c for c in db.get_cards()}
    for c in db.get_cards():
        cd = c.toDict()
        if cd['id'] not in usercards:
            usercards[cd['id']] = dict(
                user=user,
                bucket=0,
                reviewed=datetime.fromtimestamp(0),
                card=cd,
            )
    # [e['bucket'] for e in usercards.values()]
    # for id, c in cards.items():
    for c in usercards.values():
        card_descr = "/".join([e['text'] for e in c['card']['langs']])
        # print(card_descr, ':', c["bucket"])
        
    return list(usercards.values())
    

@flsk.route("/api/train-cards", methods=["GET"])
def train_cards():
    user = request.args['user']
    return jsonify(_train_cards(user))
    

@flsk.route("/api/train-card", methods=["GET"])
def train_card():
    print("selecting a random card")
    user = request.args['user']
    current = request.args.get('current')
    
    cards = [e for e in _train_cards(user) if e['card']['id']!=current]
    bucket_weights = {
        k: v for k, v in {
            0: 0.6,
            1: 0.3,
            2: 0.1,
        }.items()
        if k in [e['bucket'] for e in cards]
    }
    
    bucket = random.choices(list(bucket_weights.keys()), weights=list(bucket_weights.values()), k=1)[0]
    print('random bucket:', bucket)
    bucket_cards = [e for e in cards if e["bucket"] == bucket]
    
    card = random.choices(bucket_cards, k=1)[0]
    print("-> card: ", describe_card(card['card']['id']))
    return jsonify(dict(card=card))
    
    
    
@flsk.route("/api/add-card", methods=["POST"])
def add_card():
    is_new = request.json.get('isNew', False)
    c = conv.structure(request.json['card'], Card)
    print('SAVE CARD', c, is_new)
    # logging.exception("exception log")
    if is_new:
        try:
            db.add_card(c)
        except:
            already = db.find_similar_card(c)
            return jsonify(dict(card=already.toDict())), 400
    else:
        db.update_card(c)
    return "ok", 200

@flsk.route("/api/delete-card", methods=["POST"])
def delete_card():
    c = conv.structure(request.json, Card).toBsonDict()
    print('DELETE CARD', c)
    # logging.exception("exception log")
    assert c["_id"] is not None and len(str(c["_id"]))
    db.db.cards.delete_one({"_id": c["_id"]})
    return "ok", 200

@flsk.route('/api/upload', methods=['POST'])
def engine():
    try:
        errors = db.insert_file(list(request.files.values())[0])
    except Exception as e:
        print('----------------------------------')
        print(e)
        eventslog.error(f'upload failed: {e}')
        raise e
    return jsonify(errors), 200

@flsk.route("/api/langs", methods=["GET"])
def get_langs():
    return jsonify([
        {"id": lid, "title": ltitle} for lid, ltitle in
        [
            # ("en", "English"),
            ("fr", "Français"),
            ("fa", "فارسی"),
            # ("fe", "fenglish")
        ]
    ])


@flsk.route('/', defaults={'path': ''})
@flsk.route('/<path:path>')
def index(path):
    return render_template('index.html')

root_url = os.path.join('/', "/mikarezoo-flashcards")
static_url_path = os.path.join(root_url, "static")

app = Flask(__name__, static_url_path=static_url_path)
app.register_blueprint(flsk, url_prefix=root_url)
cache.init_app(app)


db.connect()
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    logging = app.logger
