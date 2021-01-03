from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Field cannot be blank'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Field cannot be blank'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'item with name {name} exists already.'}, 400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = data['price']
                item.store_id = data['store_id']

            except:
                return {'message':"An error ocurred updating the item"}, 500
        else:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message":"An error ocurred inserting the item"}, 500

        item.save_to_db()
        return item.json()

    


class ItemList(Resource):
    def get(self):
        return {'items':[ item.json() for item in ItemModel.query.all()]}


        