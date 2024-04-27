import flask

from . import db_session
from .items import Item
from flask import jsonify, request, make_response

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/items')
def get_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Item).all()
    return jsonify(
        {
            'items':
                [item.to_dict(only=('name', 'price', 'price_down', 'size', 'type_wear')) 
                 for item in items if item.to_dict()['is_see']]
        }
    )


@blueprint.route('/api/items', methods=['POST'])
def create_item():
    if not request.json:
        return make_response(jsonify({'error': 'Пустой запрос'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'img', 'price', 'price_down', 'size', 'count', 'type_wear', 'code']):
        return make_response(jsonify({'error': 'Неправильный запрос'}), 400)
    elif request.json['code'] != '555':
        return make_response(jsonify({'error': 'Ошибка доступа'}), 400)
    db_sess = db_session.create_session()
    item = Item(
        name=request.json['name'],
        img=request.json['img'],
        price=request.json['price'],
        price_down=request.json['price_down'],
        size=request.json['size'],
        count=request.json['count'],
        type_wear=request.json['type_wear']
    )
    db_sess.add(item)
    db_sess.commit()
    return jsonify({'id': item.id})


@blueprint.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    db_sess = db_session.create_session()
    item_id, code = item_id.split('_')
    item_id = int(item_id)
    item = db_sess.query(Item).get(item_id)
    print(item_id, code)
    if not item:
        return make_response(jsonify({'error': 'Не найдено'}), 404)
    elif code != '555':
        return make_response(jsonify({'error': 'Ошибка доступа'}), 400)
    db_sess.delete(item)
    db_sess.commit()
    return jsonify({'success': 'OK'})
