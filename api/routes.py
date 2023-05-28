from api import app, j1
from flask import render_template, redirect, request, jsonify, url_for 
from PIL import Image, ImageFilter
import os, sys
import mimetypes
import boto3
from flask_s3 import FlaskS3
from flask_cors import CORS, cross_origin

BOOSTS = j1.BOOSTS
SHOE_MODEL = j1.SHOE_MODEL
BOOST_ATTRIBUTES = j1.BOOST_ATTRIBUTES
SOLES = j1.SOLES
SWOOSHES = j1.SWOOSHES
BACKS = j1.BACKS
TOPS = j1.TOPS
TOES = j1.TOES
BODIES = j1.BODIES
PIECES = j1.PIECES
EJ = j1.EJ

s3 = boto3.resource('s3')

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/api/testpage/<token_id>')
@cross_origin()
def testpage(token_id):
    token_id = int(token_id, 0)
    num_boosts = len(BOOSTS)
    boost = BOOSTS[token_id % num_boosts]
    description = "rare colorway"
    sole = SOLES[token_id % len(SOLES)]
    swoosh = SWOOSHES[token_id % len(SWOOSHES)]
    back = BACKS[token_id % len(BACKS)]
    body = BODIES[token_id % len(BODIES)]
    top = TOPS[token_id % len(TOPS)]
    toe = TOES[token_id % len(TOES)]
    BOOST_ATTRIBUTES[0] = BOOST_ATTRIBUTES[0] + int(str(token_id)[0])
    image_url = _compose_image(['images/images/factory/top/top_%s.png' % top,
                                'images/images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/images/factory/back/back_%s.png' % back,
                                'images/images/factory/panels/panels_%s.png' % body,
                                'images/images/factory/swoosh/swoosh_%s.png' % swoosh,
                                'images/images/factory/toe/toe_%s.png' % toe ],
                               token_id, "shoe")

    attributes = []
    _add_attribute(attributes, 'sole', SOLES, token_id, display_type="sole")
    _add_attribute(attributes, 'swoosh', SWOOSHES, token_id, display_type="swoosh")
    _add_attribute(attributes, 'back', BACKS, token_id, display_type="back")
    _add_attribute(attributes, 'body', BODIES, token_id, display_type="body")
    _add_attribute(attributes, 'top', TOPS, token_id, display_type="top")
    _add_attribute(attributes, 'toe', TOES, token_id, display_type="toe")
    _add_attribute(attributes, 'boost', BOOST_ATTRIBUTES, token_id, display_type="boost_number")

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,
        'sole': sole,
        'swoosh': swoosh,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back,        
    }
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return render_template('shoe.html', data=data)

@app.route('/api/custom/testpage/<token_id>')
@cross_origin()
def custom_testpage(token_id):
    token_id = int(token_id, 0)
    description = "rare colorway"
    boost = ''
    sole = request.args.get('sole', 'ffffff')
    swoosh = request.args.get('swoosh', 'ffffff')
    back = request.args.get('back', 'ffffff')
    body = request.args.get('body', 'ffffff')
    top = request.args.get('top', 'ffffff')
    toe = request.args.get('toe', 'ffffff')

    image_url = _compose_image(['images/images/factory/top/top_%s.png' % top,
                                'images/images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/images/factory/back/back_%s.png' % back,
                                'images/images/factory/panels/panels_%s.png' % body,
                                'images/images/factory/swoosh/swoosh_%s.png' % swoosh,
                                'images/images/factory/toe/toe_%s.png' % toe],
                               token_id, "shoe")

    attributes = []
    _add_attribute_custom(attributes, 'sole', sole, token_id)
    _add_attribute_custom(attributes, 'swoosh', swoosh, token_id)
    _add_attribute_custom(attributes, 'back', back, token_id)
    _add_attribute_custom(attributes, 'body', body, token_id)
    _add_attribute_custom(attributes, 'top', top, token_id)
    _add_attribute_custom(attributes, 'toe', toe, token_id)

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,
        'sole': sole,
        'swoosh': swoosh,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back        
    }
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return render_template('shoe.html', data=data)

#/api/custom/<token_id>/?sole=000000&swoosh=FFFFFF&back=000000&body=FFFFFF&top=000000&toe=FFFFFF
@app.route('/api/custom/<token_id>/')
@cross_origin()
def custom(token_id):
    token_id = int(token_id)
    description = "Custom Colorway"
    boost = ''
    sole = request.args.get('sole', 'ffffff')
    swoosh = request.args.get('swoosh', 'ffffff')
    back = request.args.get('back', 'ffffff')
    body = request.args.get('body', 'ffffff')
    top = request.args.get('top', 'ffffff')
    toe = request.args.get('toe', 'ffffff')

    image_url = _compose_image(['images/factory/top/top_%s.png' % top,
                                'images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/factory/back/back_%s.png' % back,
                                'images/factory/panels/panels_%s.png' % body,
                                'images/factory/swoosh/swoosh_%s.png' % swoosh,
                                'images/factory/toe/toe_%s.png' % toe],
                               token_id, "custom")

    attributes = []
    _add_attribute_custom(attributes, 'sole', sole, token_id)
    _add_attribute_custom(attributes, 'swoosh', swoosh, token_id)
    _add_attribute_custom(attributes, 'back', back, token_id)
    _add_attribute_custom(attributes, 'body', body, token_id)
    _add_attribute_custom(attributes, 'top', top, token_id)
    _add_attribute_custom(attributes, 'toe', toe, token_id)

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,
        'sole': sole,
        'swoosh': swoosh,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back       
    }
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return jsonify(data)

@app.route('/api/piece/<token_id>')
@cross_origin()
def piece(token_id):
    token_id = int(token_id, 0)
    piece = PIECES[token_id % len(PIECES)]
    return ""


# endpoint for creation of single shoe
@app.route('/api/shoe/<token_id>')
@cross_origin()
def shoe(token_id):
    token_id = int(token_id, 0)
    description = "rare colorway"
    num_boosts = len(BOOSTS)
    boost = BOOSTS[token_id % num_boosts]
    BOOST_ATTRIBUTES[0] = BOOST_ATTRIBUTES[0] + int(str(token_id)[0])
    sole = SOLES[token_id % len(SOLES)]
    swoosh = SWOOSHES[token_id % len(SWOOSHES)]
    back = BACKS[token_id % len(BACKS)]
    body = BODIES[token_id % len(BODIES)]
    top = TOPS[token_id % len(TOPS)]
    toe = TOES[token_id % len(TOES)]
    image_url = _compose_image(['images/factory/top/top_%s.png' % top,
                                'images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/factory/back/back_%s.png' % back,
                                'images/factory/panels/panels_%s.png' % body,
                                'images/factory/swoosh/swoosh_%s.png' % swoosh,
                                'images/factory/toe/toe_%s.png' % toe],
                               token_id, "shoe")

    attributes = []
    _add_attribute(attributes, 'sole', SOLES, token_id)
    _add_attribute(attributes, 'swoosh', SWOOSHES, token_id)
    _add_attribute(attributes, 'back', BACKS, token_id)
    _add_attribute(attributes, 'body', BODIES, token_id)
    _add_attribute(attributes, 'top', TOPS, token_id)
    _add_attribute(attributes, 'toe', TOES, token_id)
    _add_attribute(attributes, 'boost', BOOSTS, token_id)
    _add_attribute(attributes, 'boost attribute', BOOST_ATTRIBUTES, token_id)

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,

        'sole': sole,
        'swoosh': swoosh,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back,
         
    }
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return jsonify(data)


@app.route('/api/ej1/<token_id>')
@cross_origin()
def ej1(token_id):
    token_id = int(token_id, 0)
    description = "rare colorway"
    num_boosts = len(BOOSTS)
    boost = BOOSTS[token_id % num_boosts]
    BOOST_ATTRIBUTES[0] = BOOST_ATTRIBUTES[0] + int(str(token_id)[0])
    sole = SOLES[token_id % len(SOLES)]
    ej = EJ[token_id % len(EJ)]
    back = BACKS[token_id % len(BACKS)]
    body = BODIES[token_id % len(BODIES)]
    top = TOPS[token_id % len(TOPS)]
    toe = TOES[token_id % len(TOES)]
    image_url = _compose_image(['images/factory/top/top_%s.png' % top,
                                'images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/factory/back/back_%s.png' % back,
                                'images/factory/panels/panels_%s.png' % body,
                                'images/factory/ej/ej_%s.png' % ej,
                                'images/factory/toe/toe_%s.png' % toe],
                               token_id, 'ej1')

    attributes = []
    _add_attribute(attributes, 'sole', SOLES, token_id)
    _add_attribute(attributes, 'ej', EJ, token_id)
    _add_attribute(attributes, 'back', BACKS, token_id)
    _add_attribute(attributes, 'body', BODIES, token_id)
    _add_attribute(attributes, 'top', TOPS, token_id)
    _add_attribute(attributes, 'toe', TOES, token_id)
    _add_attribute(attributes, 'boost', BOOSTS, token_id)
    _add_attribute(attributes, 'boost attribute', BOOST_ATTRIBUTES, token_id)

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,

        'sole': sole,
        'ETH': ej,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back,
         
    }
    swoosh = ej
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return jsonify(data)

@app.route('/api/ej1/testpage/<token_id>')
@cross_origin()
def ej1_test(token_id):
    token_id = int(token_id, 0)
    description = "rare colorway"
    num_boosts = len(BOOSTS)
    boost = BOOSTS[token_id % num_boosts]
    BOOST_ATTRIBUTES[0] = BOOST_ATTRIBUTES[0] + int(str(token_id)[0])
    sole = SOLES[token_id % len(SOLES)]
    ej = EJ[token_id % len(EJ)]
    back = BACKS[token_id % len(BACKS)]
    body = BODIES[token_id % len(BODIES)]
    top = TOPS[token_id % len(TOPS)]
    toe = TOES[token_id % len(TOES)]
    image_url = _compose_image(['images/factory/top/top_%s.png' % top,
                                'images/factory/sole_laces/sole_laces_%s.png' % sole,
                                'images/factory/back/back_%s.png' % back,
                                'images/factory/panels/panels_%s.png' % body,
                                'images/factory/ej/ej_%s.png' % ej,
                                'images/factory/toe/toe_%s.png' % toe],
                               token_id, 'ej1')

    attributes = []
    _add_attribute(attributes, 'sole', SOLES, token_id)
    _add_attribute(attributes, 'ej', EJ, token_id)
    _add_attribute(attributes, 'back', BACKS, token_id)
    _add_attribute(attributes, 'body', BODIES, token_id)
    _add_attribute(attributes, 'top', TOPS, token_id)
    _add_attribute(attributes, 'toe', TOES, token_id)
    _add_attribute(attributes, 'boost', BOOSTS, token_id)
    _add_attribute(attributes, 'boost attribute', BOOST_ATTRIBUTES, token_id)

    data = {
        'name': SHOE_MODEL,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes,
        'token_id': token_id,
        'boost': boost,

        'sole': sole,
        'ETH': ej,
        'body': body,
        'top': top,
        'toe': toe,
        'back': back,
         
    }
    swoosh = ej
    _store_s3(str(token_id), image_url, SHOE_MODEL, description, sole, swoosh, body, top, toe, back, boost)
    return render_template('shoe.html', data=data)

# endpoint to create shoebox
@app.route('/api/box/<token_id>')
@cross_origin()
def box(token_id):
    token_id = int(token_id, 0)
    image_url = _compose_image(['images/jordan_box_placeholder.png'], token_id, "box")

    attributes = []
    _add_attribute(attributes, 'number_inside', [3], token_id)

    return jsonify({
        'name': "Shoe Box",
        'description': "This box contains some New Jordans! It can also be traded!",
        'image': image_url,

        #TODO
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes
    })

# endpoint to create lootbox that contain shoeboxes
@app.route('/api/factory/<token_id>')
@cross_origin()
def factory(token_id):
    token_id = int(token_id, 0)
    if token_id == 0:
        name = "One Box"
        description = "When you purchase this option, you will receive a single pair of new Jordans of a random variety. " \
                      "Enjoy and take good care of your new kicks!"
        image_url = _compose_image(['images/jordan_box_placeholder.png'], token_id, "factory")
        num_inside = 1
    elif token_id == 1:
        name = "Four Boxes"
        description = "When you purchase this option, you will receive 4 new pairs of Jordans of random varieties. " \
                      "Enjoy and take good care of your new kicks!"
        image_url = _compose_image(['images/jordan_box_placeholder.png'], token_id, "factory")
        num_inside = 4
    elif token_id == 2:
        name = "One Sneakrcred Lootbox"
        description = "When you purchase this option, you will receive a lootbox with 3 new pairs of Jordans of random varieties. " \
                      "Enjoy and take good care of your new kicks!"
        image_url = _compose_image(['images/jordan_box_placeholder.png'], token_id, "factory")
        num_inside = 3

    attributes = []
    _add_attribute(attributes, 'number_inside', [num_inside], token_id)

    return jsonify({
        'name': name,
        'description': description,
        'image': image_url,
        'external_url': 'http://sneakrcred.s3.amazonaws.com/%s.png' % token_id,
        'attributes': attributes
    })


def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': options[token_id % len(options)]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)

def _add_attribute_custom(existing, attribute_name, color, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': color
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)

# create and save image
def _compose_image(image_files, token_id, path):
    composite = None
    for image_file in image_files:
        foreground = Image.open(image_file).convert("RGBA")

        if composite:
            composite = Image.alpha_composite(composite, foreground)
        else:
            composite = foreground
        output_path = "static/output/" + path + "/%s.png" % token_id 
        composite.save(output_path)
    return output_path

def _store_s3(token_id, output_path, name, description, sole, swoosh, body, top, toe, back, boost):
    s3 = boto3.client('s3')
    FILE_NAME = str(token_id) + ".png"
    s3.upload_file(
        output_path, 'sneakrcred', FILE_NAME,
        ExtraArgs = {'Metadata': { 'name' : name,
                                   'token-id' : token_id,
                                   'desctiption' : description,
                                   'sole': sole,
                                   'swoosh': swoosh,
                                   'body': body,
                                   'top': top,
                                   'toe': toe,
                                   'back': back,
                                   'boost': boost
                                   }}
    )
