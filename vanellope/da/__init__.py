#! /usr/bin/env python
# coding=utf-8
# "da" means Data Access, this file contains various quick (or dirty) methods 
# for accessing data.
#
#
import datetime
from vanellope import db
from vanellope import constant as cst

from vanellope.model import Member
from vanellope.model import Article

def get_member_by_name(_name):
    entity = db.member.find_one({"name": _name})
    if entity:
    	return Member(entity=entity)
    else:
    	return None

def get_member_by_name_lower(_name_lower):
    entity = db.member.find_one({"name_safe": _name_lower})
    if entity:
        return entity
    else:
        return None

def get_member_by_uid(_uid):
    return db.member.find_one({"uid": int(_uid)})

# this maybe dangerous, should reconsider it.
def get_member_by_secret_key(key):
    return db.member.find_one({"secret_key":key})

def get_member_by_email_lower(_email):
    return db.member.find_one({"email": _email.lower()})

def total_member():
    return db.member.count()

def insert_new_member(_entry):
    db.member.insert(_entry)

def save_member(_entry):
    db.member.save(_entry)



# Article manipulation
def get_article_by_sn(sn):
    # This is NOT MongoDB _id
    # sn is short for Serial Number
    article = db.article.find_one({"sn":int(sn)})
    if not article:
        return None
    else:
        return article

def normal_articles(skip=None, limit=None):
    # return a dict list, sort by date descending.
    cursor = db.article.find({"status": cst.NORMAL}).sort("date", -1)
    if cursor:
        if skip:
            cursor.skip(skip)
        if limit:
            cursor.limit(limit)
        return [i for i in cursor]
    else:
        return []

def deleted_or_normal_articles(_uid, status):
    cursor = db.article.find({"author": _uid, 
                            "status":status}).sort("date", -1)
    if cursor:
        return [i for i in cursor]
    else:
        return []

def get_articles_by_author(_uid):
    # Return a iterable object containning all the normal state article
    # belong to the author
    x = db.article.find({"author": int(_uid),
                        "status": cst.NORMAL}).sort("date", -1)
    if x:
        return [i for i in x]
    else:
        return []

def heat_article_by_sn(_sn):
    article = db.article.find_one({"sn": int(_sn)})
    article['heat'] += 1
    db.article.save(article)

def get_author(_uid):
    member = db.member.find_one({"uid": int(_uid)})
    if not member:
        return None
    else:
        return member

def find_adjoins(current_date):
    try:
        pre = db.article.find({"status":cst.NORMAL, 'date':
            {'$lt': current_date}}).sort("date",-1)[0]['sn']
    except:
        pre = None
    try:
        fol = db.article.find({"status":cst.NORMAL, 'date': 
            {"$gt": current_date}}).sort("date", 1)[0]['sn']
    except:
        fol = None
    return (pre, fol)


def split_pages(author=None, per=10, status=None, page=1):
    # Split all the available article into pages.

    if not status:
        status = cst.NORMAL

    if author:
        cursor = db.article.find({"author": author, "status": status})
    else:
        cursor = db.article.find({"status": status})

    copy = cursor.clone()
    total = cursor.sort("date", -1).count()
    pages =  total // int(per) + 1
    if int(page) > pages:
        page = pages # the 'page' has a max limit.
    skip = (int(page) - 1)*int(per)
    
    if total % int(per) > 0:
        pages += 1
    current = copy.sort("date", -1).skip(skip).limit(int(per))
    temp = []
    for i in current:
        temp.append(i)
    return dict(
        total = total, # articles total number
        pages = pages, 
        articles = temp,
    )






# Comment manipulation
def remove_comments_with_article(article_sn):
    db.comment.remove({"article": int(article_sn)})

def get_comment_list_by_sn(article_sn):
    cursor = db.comment.find({'article': int(article_sn)}).sort('date',1)
    comments = []
    for comment in cursor:
        comment['date'] += datetime.timedelta(hours=8)
        comment['date'] = comment['date'].strftime("%Y-%m-%d %H:%M")
        comments.append(comment)
    return comments




# Message Manipulation
#

def get_messages_by_peer(peer_list):
    # Return a iterable object
    cursor = db.message.find({"peer": {"$all": peer_list}}).sort("date", -1)
    msgs = []
    for m in cursor:
        msgs.append(dict(
            sender = m.sender,
            receiver = m.receiver,
            status = m.status,
            date = m.date,
            body = m.body,
        ))
    return msgs


def get_new_messages(uid):
    # You are the receiver
    msgs =  db.message.find({"receiver": int(uid),
                             "status": cst.UNREAD}).sort("date", 1)
    t = []
    for msg in msgs:
        m = Member(db.member.find_one({"uid": msg['sender']}))
        msg['sender'] = dict(
            name = m.name,
            uid = m.uid,
            avatar = m.avatar
        )
        msg['date'] = (msg['date'] + 
                       datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") 
        t.append(msg)
    return t

def my_all_messages(uid):
    # get all messages with sender id or receiver id is uid
    msgs = db.message.find({"peer": {"$all":[int(uid),]}}).sort("date", 1)
    t = []
    for msg in msgs:
        # You are the receiver
        if msg['receiver'] == int(uid) and msg['status'] == cst.UNREAD:
            msg['status'] = cst.READ
            db.message.save(msg)
        m = Member(db.member.find_one({"uid": msg['sender']}))
        msg['sender'] = dict(
            name = m.name,
            uid = m.uid,
            avatar = m.avatar
        )
        msg['date'] = (msg['date'] + 
                       datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M") 
        t.append(msg)
    return t

def unread_messages(receiver_id):
    # Return total unread message number
    return db.message.find({"receiver": receiver_id,
                            "status": cst.UNREAD}).count()

