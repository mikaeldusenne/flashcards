from pymongo import MongoClient
import werkzeug
import pandas as pd
from bson import ObjectId
import pymongo
from tempfile import TemporaryDirectory
from shutil import copyfile
import logging
from bson.json_util import loads, dumps
import yaml
from os import environ
from pprint import pprint
from dotenv import load_dotenv
from datetime import datetime
import os

from backend.src import helpers as h
from backend.src.pytypes import V, Card, CardLang, conv


if not 'MONGO_INITDB_DATABASE' in environ.keys():
    print("................ mongo environment not loaded, loading ................")
    load_dotenv('mongo/.env', override=True)
    load_dotenv('mongo/.env.dev', override=True)

def connect(
        username=environ['MONGO_INITDB_ROOT_USERNAME'],
        password=environ['MONGO_INITDB_ROOT_PASSWORD']):
    global client, db, projects, users
    client = MongoClient(host=environ['MONGO_HOST'],
                         port=int(environ.get('MONGO_PORT', 27017)),
                         username=username,
                         password=password,
                         authSource=environ['MONGO_INITDB_DATABASE']
                         )
    db = client[environ['MONGO_INITDB_DATABASE']]
    return db

connect()

def find_similar_card(c):
    print('looking for a similar card to', c)
    already = db.cards.find_one({"langs": {'$elemMatch': {"text": {'$in': [e.text for e in c.langs]}}}})
    print("---->", already)
    if already is not None:
        return conv.structure(already, Card)


def add_card(c, check_already=True):
    c.created = datetime.now()
    c.modified = datetime.now()
    already = find_similar_card(c)
    if already is None:
        cd = c.toBsonDict()
        del cd['_id']
        db.cards.insert_one(cd)
    else:
        raise Exception('card already exists')

def update_card(c):
    cd = c.toBsonDict()
    if cd["_id"] == "" or cd["_id"] is None:
        add_card(c)
    else:
        c.modified = datetime.now()
        db.cards.replace_one({"_id": cd["_id"]}, c.toBsonDict(), upsert=True)


def get_cards(filtr={}):
    return [V.decode(e) for e in db.cards.find(filtr).sort([("created", pymongo.DESCENDING)])]


def load_file(filepath):
    df = pd.read_csv(filepath)
    print(df.to_dict(orient="records"))
    assert all([e in "fa fr".split() for e in df.columns])
    errors = []
    success = 0
    for e in df.to_dict(orient="records"):
        # print(e)
        texts = list(e.values())
        existing = db.cards.find_one({"langs": {'$elemMatch': {"text": {'$in': texts}}}})
        if existing is not None:
            errors.append({"file": e, "db": V.decode(existing).toDict()})
            print('already exists:', e)
        else:
            success += 1
            c = Card(langs=[CardLang(lang=lang, text=text) for lang, text in e.items()])
            add_card(c)
    
    return dict(
        success=success,
        errors=len(errors),
        errors_details=errors,
    )


def insert_file(filecontent: werkzeug.datastructures.FileStorage):
    destdir = './backend/data/'
    with TemporaryDirectory() as tmpdirname:
        filepath = os.path.join(tmpdirname, filecontent.name)
        filecontent.save(filepath)
        return load_file(filepath)

    
def create_indexes():
    db.usercards.create_index(
        [
            ("user", 1),
            ("card", 1),
        ],
        unique=True
    )
    
    


