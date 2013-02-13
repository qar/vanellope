import pymongo

def CheckAuth(cookie_auth):
    # check authorization
    conn = pymongo.Connection('localhost',27017)
    db_member = conn.page302.member
    member = db_member.find_one({'auth':  cookie_auth})
    # database return None if no such member
    if member:
        return member
    else:
        return None
        






