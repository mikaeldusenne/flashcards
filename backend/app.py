from flask import Flask, render_template, jsonify, redirect, flash, request, url_for, Response, Blueprint
import flask
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_caching import Cache
# import bcrypt
from flask_bcrypt import Bcrypt
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

from backend.src.pytypes import conv, Card, CardLang, V, Deck, User, UserAlreadyExists
import backend.src.helpers as h
import backend.src.db as db
from backend.src import loggingManager
from backend.src import MailSender

eventslog = logging.getLogger('events')

cache = Cache(config={
    # 'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': '/.flask-cache', "CACHE_DEFAULT_TIMEOUT": 9999999
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://redis',
    'CACHE_REDIS_PORT': '6379',
    "CACHE_DEFAULT_TIMEOUT": 9999999,
})


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
    if "deck" in request.args and request.args['deck'] is not None and len(request.args['deck']):
        args['decks'] = {'$elemMatch': {"$eq": request.args['deck']}}
        
    total_n = db.db.cards.count_documents(args)
    
        
    cards = db.db.cards.find(args)
    
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

def _train_cards(user, deck=None):
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
    
    usercards = {
        e["card"]['id']: e
        for e in map(prepare_user_card, usercards)
        if deck is None or deck in e['card'].get("decks", [])
    }
    
    # usercards
    # cards = {c.id: c for c in db.get_cards()}
    matchd = {}
    if deck is not None:
        matchd["decks"] = {'$elemMatch': {"$eq": deck}}
        
    for c in db.get_cards(matchd):
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
    return jsonify(_train_cards(user, request.args.get('deck')))
    

@flsk.route("/api/train-card", methods=["GET"])
def train_card():
    user = request.args['user']
    deck = request.args.get('deck')
    current = request.args.get('current')
    print("selecting a random card", user, deck)
    
    cards = [e for e in _train_cards(user, deck) if e['card']['id']!=current]
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
    
    
    
@flsk.route("/api/decks", methods=["GET", "POST", "DELETE"])
def decks():
    if request.method == "GET":
        # return jsonify([V.decode(e).toDict() for e in db.db.decks.find()])
        return jsonify(db.get_decks_with_n_cards())
    elif request.method == "POST":
        print('save deck', request.json)
        db.update_deck(conv.structure(request.json, Deck))
        return "ok", 200
    elif request.method == "DELETE":
        db.delete_deck(request.json['id'])
        return "ok", 200
    
    
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
        decks = request.args.get('decks')
        if decks is not None:
            decks = decks.split(',')
        errors = db.insert_file(list(request.files.values())[0], decks=decks)
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



############ user management

def hash_password(p):
    return bcrypt.generate_password_hash(p).decode("utf-8")



# @flsk.route('/api/register', methods=['POST'])
# def register():
#     # todo registration form
#     d = structure(request.json, User)
#     register_user_and_hash_pwd(d)
#     return "ok", 200

######## user activation

def create_user_activation_link(u, force=False):
    if force or u.activation_link is None or len(u.activation_link) == 0:
        link, _ = h.generate_activation_link(f"{u.id}")
        assert link is not None
        u.activation_link = link
        db.update_user(u.id, {'activation_link': link})
        eventslog.info(f'update user {u.id} activation link')


def register_user_and_hash_pwd(u):
    u.email = u.email.strip()
    u.password = hash_password(u.password)
    link, _ = h.generate_activation_link(f"{u.id}")
    u.activation_link = link
    db.insert_user(u)
    return u


def mkurl(*path):
    return os.path.join(environ['WEBSITE_ROOT_URL'], *path)

def send_user_activation(u):
    create_user_activation_link(u, force=False)
    print(f"******** {u.activation_link=}")
    url = mkurl("user/activate", u.activation_link)
    eventslog.info(f'sending user {u.email} activation link')
    MailSender.send_email_with_link(u.email, url)
    
    
# def create_user(u: User):
#     ''' create a user and it's activation link '''
#     u.email = u.email.strip()
#     id = db.insert_user(u)
#     create_user_activation_link(u)
#     eventslog.info(f'user {u.email} created: {id}, activation link: u.activation_link')


@flsk.route('/register', methods=['POST'])
def register():
    try:
        u = register_user_and_hash_pwd(conv.structure(request.json, User))
        send_user_activation(u)
    except UserAlreadyExists:
        return "this user already exists!", 500
    return "ok", 200


def get_user_infos(current_user):
    return {k: v for k, v in current_user.toDict().items() if k != 'password'}


@flsk.route('/user/activate/<linkid>', methods=['POST'])
def activate_user(linkid):
    u = db.get_user(filtr={'activation_link': linkid})
    eventslog.info('activating user {u.email}')
    if u is None:
        return "invalid activation link", 400
    else:
        db.update_user(u.id, {
            "active": True,
            "activation_link": "",
        })
        eventslog.info(f'user {u.id} activated')
        return "ok", 200


@flsk.route('/api/user/reset-password/<linkid>', methods=['POST'])
def reset_user_password(linkid):
    u = db.get_user(filtr={'activation_link': linkid})
    eventslog.info('resetting user password {u.email}')
    if u is None:
        return "invalid activation link", 400
    else:
        db.update_user(u.id, {
            "activation_link": "",
            "password": hash_password(request.json['password'])
        })
        eventslog.info(f'user {u.password} password reset')
        return "ok", 200


@flsk.route('/api/mail-from-activation-link', methods=['GET'])
def get_mail_from_link():
    u = db.get_user(filtr={'activation_link': request.args['link']})
    return jsonify(u.mail)


@flsk.route('/api/reset-password-send-link', methods=['GET'])
def reset_password():
    try:
        print("reset password")
        print(request.args)
        u = db.get_user(email=request.args['email'])
        print(u)
        assert u is not None and u.active, f"password reset failed: {request.args}"
        create_user_activation_link(u, force=True)
        
        url = mkurl("/user/reset-password", u.activation_link)
        eventslog.info(f'resetting user {u.email} password: sending email, activation link: {url}')
        MailSender.send_email_with_link(
            u.email,
            url,
            reason="reset your password"
        )
    except Exception as e:
        traceback.print_exc()
        logging.getLogger('errors').error(f"{e}")
    return "ok", 200



#### end of activation





@flsk.route('/login-check', methods=['GET'])
def login_check():
    u = None
    print("LOGIN CHECK")
    print(current_user)
    if current_user.is_authenticated:
        logging.info(f'already authenticated as {current_user}')
        ans = dict(
            email=current_user.email,
            admin=current_user.is_admin(),
        )
        print('********', ans)
        return jsonify(ans)
    else:
        return jsonify({})


@flsk.route('/login', methods=['POST'])
def login():
    u = None
    j = request.json
    userDb = db.get_user(email=j["email"])
    if userDb is not None:
        print(userDb, j["password"])
        password_ok = bcrypt.check_password_hash(
            userDb.password, j["password"])
        if password_ok:
            print("LOGIN OK", userDb.email)
            userDb.authenticated = True
            login_user(userDb, remember=True)
            print(f'**************************** {userDb.id} logged in')
            
            return jsonify(
                dict(
                    email=current_user.email,
                    admin=current_user.is_admin(),
                )), 200
        
    
    eventslog.info(f'{j["email"]} failed to log in (wrong username/password)')
    return "Invalid credentials", 401


@flsk.route("/logout", methods=["GET"])
@login_required
def logout():
    eventslog.info(f'{current_user.id} logged out')
    logout_user()
    return jsonify("ok")




################# end of user management















@flsk.route('/', defaults={'path': ''})
@flsk.route('/<path:path>')
def index(path):
    return render_template('index.html')

root_url = os.path.join('/', "/mikarezoo-flashcards")
static_url_path = os.path.join(root_url, "static")

app = Flask(__name__, static_url_path=static_url_path)
app.register_blueprint(flsk, url_prefix=root_url)
cache.init_app(app)
app.secret_key = environ['FLASK_SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)
else:
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    # logging = app.logger
