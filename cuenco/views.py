import md5
from cuenco import app, db
from cuenco.models import WebLink
from flask import request, url_for, render_template, redirect, jsonify
from urlparse import urlparse
from sqlalchemy import func 
from datetime import datetime

#base-62 encode a number
def encode(num):
    if num < 1: raise Exception("encode: Number must be positive.")
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(charset)
    encoding = ''
    
    while num > 0:
        i = num % base
        encoding = charset[i] + encoding
        num = (num - i) / base
        
    return encoding

@app.route('/')
def index():
    return render_template('search_box.html')
    
@app.route('/<url_hash>')
def link_redirect(url_hash):
    existing_link = WebLink.query.filter_by(url_hash = url_hash).first()
    if (existing_link is None):
        return render_template('404.html'), 404
    else:
        existing_link.views += 1
        db.session.commit()
        return redirect(existing_link.long_url)
    
@app.route('/recent')
def recent_entries():
    entries = WebLink.query.order_by(WebLink.date.desc()).limit(10)
    return render_template('links.html', entries=entries, header="Recent")

@app.route('/popular')
def popular_entries():
    entries = WebLink.query.order_by(WebLink.views.desc()).limit(10)
    return render_template('links.html', entries=entries, header="Popular")
    
@app.route('/_urlgen', methods=['POST'])
def generate_short_url():
    link = WebLink(request.form['url'])
    domain = urlparse(request.url).netloc
    
    #return invalid if the URL is invalid or contains this site's domain name
    if not link.is_valid() or urlparse(link.long_url).netloc == domain:
        return jsonify(result="Invalid URL")
    
    url_md5 = md5.new(link.long_url).hexdigest()
    existing_link = WebLink.query.filter_by(md5_hash = url_md5).first()
    if (existing_link is not None):
        result = app.config["WEBSITE_URL"] + str(existing_link.url_hash)
    else:
        id_next = int(db.session.query(func.max(WebLink.id))[0][0] or 0) + 1
        hash_num = (2654435761 * id_next) % 4294967296 #perfect hash function
        link.url_hash = encode(hash_num)
        link.md5_hash = url_md5
        link.date = datetime.now()
        db.session.add(link)
        db.session.commit()
        result = app.config["WEBSITE_URL"] + "/" + link.url_hash
        
    return jsonify(result=result)
