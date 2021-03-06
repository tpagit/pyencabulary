from flask import Blueprint

from server.api.auth.login import LoginAPI
from server.api.auth.logout import LogoutAPI
from server.api.dictionary.words import WordAPI
from server.api.dictionary.translations import TranslationsAPI
from server.api.dictionary.learn import LearnAPI
from server.api.dictionary.words_datatable import WordsDataTableAPI
from server.api.dictionary.autocomplete import AutoCompleteAPI

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.add_url_rule('/api/login', view_func=LoginAPI.as_view('login'), methods=['POST'])
api_blueprint.add_url_rule('/api/logout', view_func=LogoutAPI.as_view('logout'), methods=['POST'])

word_api_view = WordAPI.as_view('word')
api_blueprint.add_url_rule('/api/word', view_func=word_api_view, methods=['POST'])
api_blueprint.add_url_rule('/api/word/<int:id_word>', view_func=word_api_view, methods=['PUT', 'GET', 'DELETE'])

translation_api_view = TranslationsAPI.as_view('translation')
api_blueprint.add_url_rule('/api/translation', view_func=translation_api_view, methods=['POST'])
api_blueprint.add_url_rule('/api/translation/<int:id_translation>', view_func=translation_api_view,
                           methods=['GET', 'PUT', 'DELETE'])

learn_api_view = LearnAPI.as_view('learn')
api_blueprint.add_url_rule('/api/learn', view_func=learn_api_view, methods=['GET', 'POST'])

api_blueprint.add_url_rule('/api/words/jqdatatable', view_func=WordsDataTableAPI.as_view('words_jqdatatable'),
                           methods=['POST'])

autocomplete_api_view = AutoCompleteAPI.as_view('autocomplete')
api_blueprint.add_url_rule('/api/autocomplete/<string:word>', view_func=autocomplete_api_view, methods=['GET'],
                           defaults={'id_word_type': None})
api_blueprint.add_url_rule('/api/autocomplete/<string:word>/<int:id_word_type>', view_func=autocomplete_api_view,
                           methods=['GET'])
