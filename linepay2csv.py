import typing as tp
import pyparsing as pp
import re

def repr(className: str, **kwargs) :
    fmtArg = ' '.join("{}={}".format(key, kwargs[key]) for key in kwargs)
    return "<{} {}>".format(className, fmtArg)

class PayDate :
    def __init__(self, vars) :
        self.year  = int(vars[0])
        self.month = int(vars[2])
        self.day   = int(vars[4])
    def __repr__(self) :
        return repr("PayDate", year=self.year, month=self.month, day=self.day)

YEAR  = pp.Word(pp.nums, min=4, max=4)
MONTH = pp.Word(pp.nums, min=2, max=2)
DAY   = MONTH
WEEK  = pp.Regex("[月火水木金土日]曜日").suppress()
PAY_DATE = pp.Group(pp.LineStart() + YEAR + pp.Literal('.') + MONTH + pp.Literal('.') + DAY).setParseAction(PayDate)

HOUR  = MONTH
MINUS = MONTH
class PayTime :
    def __init__(self, vars) :
        self.hour  = vars[0]
        self.minus = vars[2]
    def __repr__(self) :
        return repr('PayTime', hour=self.hour, minus=self.minus)
PAY_TIME = (HOUR + pp.Literal(':') + MINUS).setParseAction(PayTime)

class Yen :
    def __init__(self, vars) :
        self.yen = self._parse(vars[0])    
    def _parse(self, s : str) :
        return int(s.replace(',', ""))
    def __repr__(self) :
        return repr('Yen', yen=self.yen)
YEN = (pp.Regex(r'\b\d{1,3}(,\d{3})*\b') + pp.Literal('円')).setParseAction(Yen)

class KeyValue :
    def __init__(self, vars) :
        pair = vars[0].split(': ')
        self.key   = pair[0]

        if len(vars) >= 2 and type(vars[1]) == Yen :
            self.value = vars[1]
        else :
            self.value = pair[1]
    def __repr__(self) :
        return repr("KeyValue", key=self.key, value=self.value)
KEY_VALUE     = (pp.Regex(".+: ") + YEN | pp.Regex(".+: .+")).setParseAction(KeyValue)
KEY_VALUE_REC = pp.lineStart + KEY_VALUE + pp.lineEnd


# === お支払い ===
class ActionOshiharai : 
    def __init__(self, vars) :
        self.yen    = vars[0]
        self.values = vars[1]
    def __repr__(self) :
        return repr("ActionOshiharai", values=self.values)
OSHIHARAI_DONE   = pp.Suppress('お支払いが完了しました。')
ACTION_OSHIHARAI = (pp.Suppress("お支払い") + YEN + OSHIHARAI_DONE + pp.Group(pp.OneOrMore(KEY_VALUE))).setParseAction(ActionOshiharai)

WALETTE_LITERAL = pp.Suppress('LINEウォレット LINE Pay')

ACTION = PAY_TIME + WALETTE_LITERAL + ACTION_OSHIHARAI


ret = ACTION.parseString(s)
print(ret)

#with open("[LINE]LINEウォレット", "r", encoding="utf-8") as h :
#    pass
