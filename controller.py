from flask import Flask, request
from flask_restful import Api, Resource

from service import Service

# Flask initialisation
app = Flask(__name__)
app.debug = True
api = Api(app)


# for user input query string
class QueryResults(Resource):
    @staticmethod
    def get():
        try:
            return Service.getResults(query_string=request.args['query'], top_n=request.args['n'])
        except Exception as error:
            return "Error - " + str(error)


# for each result players stat
class PlayerStats(Resource):
    @staticmethod
    def get(player):
        try:
            return Service.getPlayerStats(player=player)
        except Exception as error:
            return "Error - " + str(error)


api.add_resource(QueryResults, '/query')
api.add_resource(PlayerStats, '/player/<string:player>/stats')

if __name__ == '__main__':
    app.run()