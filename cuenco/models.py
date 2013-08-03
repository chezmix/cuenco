import re
from cuenco import db

class WebLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(512))
    url_hash = db.Column(db.String(10), unique=True)
    md5_hash = db.Column(db.String(32), unique=True)
    views = db.Column(db.Integer, unique=False, default=0)
    date = db.Column(db.DateTime, unique=False)

    def __init__(self, long_url=""):
        self.long_url = long_url

    def __repr__(self):
        return '<WebLink %r>' % self.long_url
        
    def is_valid(self):
        #Django's regex for URL validation
        regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
                r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                
        if regex.match(self.long_url):
            return True
        else:
            return False
            