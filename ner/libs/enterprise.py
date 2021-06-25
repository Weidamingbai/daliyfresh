import  re
from libs.pii import Pii

class Enterprise:
    # 统一社会信用代码校验算法 True 表示通过校验，否则False 表示不通过校验
    def check_credit(value):
        credit_str = value.upper()
        credit_pattern = r'^(1[129]|5[1239]|9[123]|Y1)\d{6}[\dA-Z]{8}[X\d][\dA-Z]$'
        if len(credit_str) != 18:
            return False
        search = re.search(credit_pattern, credit_str, re.S)
        if search:
            # if check_organization(xinyong_str[8:17]):
            str_to_num = {
                'A': 10,
                'B': 11,
                'C': 12,
                'D': 13,
                'E': 14,
                'F': 15,
                'G': 16,
                'H': 17,
                'J': 18,
                'K': 19,
                'L': 20,
                'M': 21,
                'N': 22,
                'P': 23,
                'Q': 24,
                'R': 25,
                'T': 26,
                'U': 27,
                'W': 28,
                'X': 29,
                'Y': 30}
            num_to_str = {
                10: 'A',
                11: 'B',
                12: 'C',
                13: 'D',
                14: 'E',
                15: 'F',
                16: 'G',
                17: 'H',
                18: 'J',
                19: 'K',
                20: 'L',
                21: 'M',
                22: 'N',
                23: 'P',
                24: 'Q',
                25: 'R',
                26: 'T',
                27: 'U',
                28: 'W',
                29: 'X',
                30: 'Y'}
            verify_code = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
            verify_code = 31 - sum([(str_to_num.get(credit_str[index], 0) if credit_str[index].isalpha(
            ) else int(credit_str[index])) * verify_code[index] for index in range(17)]) % 31
            verify_code = num_to_str.get(
                verify_code, '') if verify_code > 9 else verify_code
            if str(verify_code) == value[-1]:
                return True
            else:
                return False
        else:
            return False


    # 营业执照号码校验算法 True 表示通过校验，否则False 表示不通过校验
    def check_business(value):
        business_pattern = r'^\d{15}$'
        if re.search(business_pattern, value, re.S):
            verify_code = 10
            for index in range(14):
                verify_code = (
                    ((verify_code % 11 + int(value[index])) % 10 or 10) * 2) % 11
            verify_code = (11 - (verify_code % 10)) % 10
            if str(verify_code) == value[-1]:
                return True
            else:
                return False
        else:
            return False


    # 组织机构代码校验算法 True 表示通过校验，否则False 表示不通过校验
    def check_organization(value):
        organization_str = value.upper().replace('-', '')
        organization_pattern = r'^[\dA-Z]{8}[X\d]$'
        if re.search(organization_pattern, organization_str, re.S):
            verify_code = [3, 7, 9, 10, 5, 8, 4, 2]
            verify_code = 11 - sum([int((ord(organization_str[index]) - 55) if organization_str[index].isalpha()
                                        else organization_str[index]) * verify_code[index] for index in range(8)]) % 11
            verify_code = 'X' if verify_code == 10 else (
                '0' if verify_code == 11 else str(verify_code))
            if verify_code == organization_str[-1]:
                return True
            else:
                return False
        else:
            return False

    # 税务登记号码校验算法  用到了身份校验算法和组织机构校验算法
    def check_tax(shuiwu_str):
        '''税务登记证号码，使用了校验位算法'''
        shuiwu_str = shuiwu_str.upper()
        if len(shuiwu_str) == 20:
            # check_id 身份证号码
            if Pii.check_IDNumber(shuiwu_str[:18]):
                if re.search(r'^[A-Z\d]{2}$', shuiwu_str[18:], re.S):
                    return True
            return False
        else:
            shuiwu_str = shuiwu_str.replace('-', '')
            search = re.search(r'^\d{6}[\dA-Z]{8}[X\d]$', shuiwu_str, re.S)
            return (True if Enterprise.check_organization(
                shuiwu_str[6:]) else False) if search else False

    @staticmethod
    def findcredit(text):
        """
        :param name: credit
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Enterprise.check_credit(text):
            return text
        return None

    @staticmethod
    def findbusiness(text):
        """
        :param name: business
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Enterprise.check_business(text):
            return text
        return None

    @staticmethod
    def findorganization(text):
        """
        :param name: organization
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Enterprise.check_organization(text):
            return text
        return None

    @staticmethod
    def findtax(text):
        """
        :param name: tax
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Enterprise.check_tax(text):
            return text
        return None