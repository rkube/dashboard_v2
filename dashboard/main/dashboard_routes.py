# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard/dashboard_routes.py

from flask import render_template, send_from_directory, request

from pymongo import MongoClient
# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
#dashboard = Blueprint("dashboard", __name__, template_folder="templates")

import json
from . import dashboard

@dashboard.route('/hello')
def hello_dashboard():
    return render_template("hello_dashboard.html")

@dashboard.route('/hello_vue')
def hello_vue():
    return send_from_directory("templates", "hello_vue.html")

@dashboard.route("/newvue")
def hello_newvue():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)


@dashboard.route("/query_db")
def new_query():
    """This path queries mongodb whether a collection with the name exists.
    Currently data analysis routines are stored in the delta-fusion database
    with collection names test_analysis_[ABCDEF], where A-F are in [A-Z][0-9].
    Each test_analysis collection has a document where the run_config for
    delta is stored.

    The end-point receives an identifier [ABCDEF] and tries to access the
    collection test_analysis_[ABCDEF]. IF it exists, it return the run_config.

    We are processing this endpoint as a request.

    Tip: Try ABC123
    """
    # Get the collection name from the request
    coll_name = request.args.get("coll_name")
    # Check if coll_name has the right length
    assert(coll_name.__len__() == 6)
    coll_name = "test_analysis_" + coll_name

    # Log in to mongo and try to find the run config for the requested run
    with open("mongo_secret", "r") as df:
        lines = df.readlines()
    mongo_uri = lines[0].strip()
    mongo_user = lines[1].strip()
    mongo_pass = lines[2].strip()

    client = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass)
    coll = client.get_database()[coll_name]
    post = coll.find_one({"run_config": {"$exists": True}})

    # We need to run the post through the json interpreter to get rid of
    # True/true mismatch between python and JS...
    s1 = post["run_config"].__str__()
    # Json expects double quotes, not single quotes
    s2 = s1.replace("\'", "\"")
    # Json expects bool with lower-case letters, not upper-case
    s3 = s2.replace("True", "true")
    # Load as json
    post_js = json.loads(s3)
    
    return json.dumps(post_js)

# End of file dashboard.py