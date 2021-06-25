from unittest import TestCase
from libs.internet import  Internet
from libs.misc import Misc
from libs.pii import Pii
from libs.enterprise import Enterprise
from libs.keys_or_token import Keys_or_token
from libs.date import Date
import pytest



class Test_internet(TestCase):
    # find 参数(识别信息，待识别文本)
    # 识别信息列表{'ip','ipv6','mac','url'}
    # 结果为一个列表 列表元素是一个[information，pos，key]的列表

    def test_ip(self):
        result = Internet.findip('192.168.1.12')
        assert result == '192.168.1.12'

    def test_ipv6(self):
        result = Internet.findipv6("0000:0000:0000:0000:0000:0000:0000:0001")
        print(result)
        assert result == '0000:0000:0000:0000:0000:0000:0000:0001'

    def test_mac(self):
        result = Internet.findmac("8C:C1:21:A2:44:A3")
        assert result == '8C:C1:21:A2:44:A3'

    def test_url(self):
        result = Internet.findurl("https://www.youtube.com/playlist?list=PL1eC1aP-LYNg2ya1ywPj0pipd0y2EWGEl")
        print(result)
        assert result == 'https://www.youtube.com/playlist?list=PL1eC1aP-LYNg2ya1ywPj0pipd0y2EWGEl'

class Test_misc(TestCase):

    def test_jdbc(self):
        result = Misc.findjdbc("jdbc:oracle:thin:127.0.0.1:1521:dbname")
        assert result == "jdbc:oracle:thin:127.0.0.1:1521:dbname"

class Test_PII(TestCase):
    # find 参数(识别信息，待识别文本)
    # 识别信息列表{"id","bankcard","phone","email","telephone","carnum","vin"}
    # 结果为一个列表 列表元素是一个[information，pos，key]的列表
    def test_id(self):
        result = Pii.findid('341222200002167694')
        assert  result == '341222200002167694'

    def test_phone(self):
        result = Pii.findphone("17862321111")
        assert  result == '17862321111'

    def test_bankcard(self):
        result = Pii.findbankcard("6228480088141848874")
        assert  result == '6228480088141848874'

    def test_email(self):
        result = Pii.findemail('11938689741@qq.com')
        assert  result == '11938689741@qq.com'

    def test_telephone(self):
        result = Pii.findtelephone('0531-5891425')
        assert  result == '0531-5891425'

    def test_carnum(self):
        result = Pii.findcarnum('京A66666')
        assert  result == '京A66666'

    def test_vin(self):
        result = Pii.findvin( 'UU6JA69691D713820')
        assert result == 'UU6JA69691D713820'

class Test_enterprise(TestCase):
    # find 参数(识别信息，待识别文本)
    # 识别信息列表{"credit","business","organization","tax"}
    # 结果为一个列表 列表元素是一个[information，pos，key]的列表
    def test_credit(self):
        result = Enterprise.findcredit('1161050056377320XW')
        assert  result == '1161050056377320XW'

    def test_business(self):
        result = Enterprise.findbusiness('330782600260687')
        assert  result == '330782600260687'


    def test_organization(self):
        result = Enterprise.findorganization('72215535-4')
        assert  result == '72215535-4'

    def test_tax(self):
        result = Enterprise.findtax('350203798097787')
        assert  result == '350203798097787'

class Test_key(TestCase):
    # find 参数(识别信息，待识别文本)
    # 识别信息列表{"MD5"}
    # 结果为一个列表 列表元素是一个[information，pos，key]的列表
    def test_MD5(self):
        result = Keys_or_token.findmd5('e10adc3949ba59abbe56e057f20f883e')
        assert result == 'e10adc3949ba59abbe56e057f20f883e'

class Test_date(TestCase):
    # find 参数(识别信息，待识别文本)
    # 识别信息列表{"date"}
    # 结果为一个列表 列表元素是一个[information，pos，key]的列表
    def test_date(self):
        result = Date.finddate('1985-04-04 05:17:26')
        assert  result == '1985-04-04 05:17:26'

if __name__ == "__main__":
    pytest.main("-s test_class")