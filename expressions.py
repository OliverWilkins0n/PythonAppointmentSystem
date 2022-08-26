from main import *
from AddCustomerSQL import *

def is_phone_number(n):
    rule = re.compile(r'^(?:\+?44)?[07]\d{10,13}$')
    if not rule.search(n):
        return False
    else:
        return True

def is_postcode(n):
    rule = re.compile(r'^([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)$')
    if not rule.search(n):
        return False
    else:
        return True
def is_email(n):
    rule = re.compile('^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$')
    if not rule.search(n):
        return False
    else:
        return True
    
def is_date(n):
    rule = re.compile('^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$')
    if not rule.search(n):
        return False
    else:
        return True
