'''
Created on 17-Nov-2016

@author: jatinbhola6
'''
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation.statement import Statement
import urllib.request
import json
class LocationAdapter(LogicAdapter):
    def __init__(self,**kwargs):
        super(LocationAdapter,self).__init__(**kwargs)
        self.client_loc=kwargs.get('loc')
        self.possible_types=['atm','bank','hotels','restaurant','movie theater','gas station','park','train station','pharmacy','hospital']
    def can_process(self,statement):
        if statement.text.startswith("#nearme") and statement.text[8:] in self.possible_types and 'loc' :
            self.type=statement.text[8:].replace(" ","_")
            self.keyw=""
            return True
        elif statement.text.startswith("#nearme") and statement.text[8:] not in self.possible_types :
            self.type=""
            self.keyw=statement.text[8:].replace(" ","_")
            return True
        return False
    
    def process(self,statement):
        if len(self.client_loc)!=2:
            return 0,Statement("location unavailable")
        else:
            confidence=1
        response=urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(self.client_loc[0])+","+str(self.client_loc[1])+"&radius=5000&type="+self.type+"&keyword="+self.keyw+"&key=AIzaSyC21aC_05Zdm7o9wUox5SM5EWYq8YKF4d8")
        data=json.loads(response.read().decode('utf-8'))
        response_str=""
        for i in range(5):
            p_id=data['results'][i]['place_id']
            ref_resp=urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?placeid="+p_id+"&key=AIzaSyC21aC_05Zdm7o9wUox5SM5EWYq8YKF4d8")
            ref_data=json.loads(ref_resp.read().decode('utf-8'))
            ref_url=ref_data['result']['url']
            response_str +='<a href="'+ref_url+'" target="_blank">'+data['results'][i]['name']+'</a><br />'
        #print(self.client_loc[1])
        return confidence,Statement(response_str)