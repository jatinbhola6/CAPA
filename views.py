from django.http import JsonResponse
from chatterbot import ChatBot
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.views.generic.base import TemplateView
from Minor import settings
from django.views.decorators.csrf import ensure_csrf_cookie

class ChatterBotAppView(TemplateView):
    template_name="Capa/app.html"
    
class ChatterBotViewMixin(object):
    
    '''panga=[
              "Capa.MyAdapters.CalcAdapter",
              "Capa.MyAdapters.WikiAdapter",
              "chatterbot.adapters.logic.ClosestMatchAdapter"
              ]
    trainer=ChatterBotCorpusTrainer
    training_data="chatterbot.corpus.english"
    chatterbot = ChatBot("Capa Bot", logic_adapters=panga)
    chatterbot.set_trainer(trainer)
    chatterbot.train(training_data)'''
    #chatterbot=ChatBot(**settings.CHATTERBOT)
    def validate(self,data):
        from django.core.exceptions import ValidationError
        if 'text' not in data:
            raise ValidationError('The attribute "text" is required.')


class ChatterBotView(ChatterBotViewMixin, TemplateView):
    
    def validate(self,data):
        from django.core.exceptions import ValidationError
        if 'text' not in data:
            raise ValidationError('The attribute "text" is required.')

    def _serialize_recent_statements(self):
        if self.chatterbot.recent_statements.empty():
            return []

        recent_statements = []

        for statement, response in self.chatterbot.recent_statements:
            recent_statements.append([statement.serialize(), response.serialize()])

        return recent_statements

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            input_data = json.loads(request.read().decode('utf-8'))
        else:
            input_data = json.loads(request.body.decode('utf-8'))
        self.validate(input_data)
        temp=settings.CHATTERBOT
        if 'loc' in input_data.keys():
            temp['loc']=input_data['loc']
            #print((temp['loc']))
        self.chatterbot=ChatBot(**temp)
        response_data = self.chatterbot.get_response(input_data)
        return JsonResponse(response_data.serialize(), status=200)

    def get(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'recent_statements': self._serialize_recent_statements()
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def patch(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def delete(self, request, *args, **kwargs):
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

