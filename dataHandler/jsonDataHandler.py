'''
Created on 9-nov.-2011

@author: cncfanatics
'''
from .dataHandler import DataHandler
import json
import bz2
import weakref
from ..fit import Type, Expression, Effect

class JsonDataHandler(DataHandler):
    '''
    JSON based dataHandler, this dataHandler will load eve staticdata and expression data into memory at instanciation from json files.
    Any call to getType or getExpression will be answered using the in-memory dictionaries.
    By default, files are assumed to be ./eos/data/eve.json.bz2 and ./eos/data/expressions.json.bz2
    Data is assumed to be encoded as UTF-8
    '''
    def __init__(self, typesPath, expressionsPath, effectsPath, encoding='utf-8'):
        self.__typesCache = weakref.WeakValueDictionary()
        self.__expressionsCache = weakref.WeakValueDictionary()
        self.__effectsCache = weakref.WeakValueDictionary()

        with bz2.BZ2File(typesPath, 'r') as f:
            self.__typeData = json.loads(f.read().decode('utf-8'))

        with bz2.BZ2File(expressionsPath, 'r') as f:
            self.__expressionData = json.loads(f.read().decode('utf-8'))

        with bz2.BZ2File(effectsPath, 'r') as f:
            self.__effectData = json.loads(f.read().decode('utf-8'))

    def getType(self, id):
        '''
        Return the type with the passed id
        '''
        type = self.__typesCache.get(id)
        if(type == None):
            # We do str(id) here because json dicts always have strings as key
            data = self.__eveData[str(id)]
            type = Type(self, id, data["group"], tuple(data["effects"]),
                        {x : y for x, y in data["attributes"]})

            self.__typesCache[id] = type

        return type;

    def getExpression(self, id):
        '''
        return the expression with the passed id
        '''
        expression = self.__expressionsCache.get(id)
        if(expression == None):
            data = self.__expressionData[str(id)]
            expression = Expression(self, id, data["operand"], data["value"], data["args"],
                                    data["typeID"], data["groupID"], data["attributeID"])

            self.__expressionsCache[id] = expression

        return expression

    def getEffect(self, id):
        '''
        return the effect with the passed id
        '''
        effect = self.__effectsCache.get(id)
        if(effect == None):
            data = self.__effectData[str(id)]
            effect = Effect(self, id, data["preExpression"], data["postExpression"],
                            data["isOffensive"], data["isAssistance"])

            self.__effectsCache[id] = effect

        return effect