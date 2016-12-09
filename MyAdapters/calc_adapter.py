from chatterbot.adapters.logic import LogicAdapter
import re
from chatterbot.conversation import Statement
class CalcAdapter(LogicAdapter):
    def __init__(self,**kwargs):
        super(CalcAdapter,self).__init__(**kwargs)
        self.req=re.compile('\d+(\.\d+)?\s*[+\-*/%]{1}\s*\d+(\.\d+)?(\s*[+\-*/%]{1}\s*\d+(\.\d+)?)*')
        self.resp=re.compile('\d+(\.\d+)?')
    def can_process(self, statement):
        if statement.text.startswith("#calc") and self.req.fullmatch(statement.text[6:]) is not None :
            print("can process")
            return True
        return False
    def process(self,statement):
        request=statement.text[6:]
        response=Statement(eval(request))
        if re.match(r'\d+(\.\d+)?',str(response.text)):
            print("processed")
            confidence=1 
        else:
            confidence=0.5
        '''
        confidence=1
        print(type(response.text))'''
        return confidence,response