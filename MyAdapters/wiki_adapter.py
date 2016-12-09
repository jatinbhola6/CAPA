from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
import wikipedia
class WikiAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(WikiAdapter, self).__init__(**kwargs)
    def can_process(self, statement):
        if statement.text.startswith("#wiki"):
            print("can process")
            return True
        
        return False
    
    def process(self, statement):
        request=statement.text[6:]
        confidence=1
        response=Statement(wikipedia.summary(request,sentences=3))
        return confidence,response