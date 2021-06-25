from datetime import datetime
import  re
class Pii:
    # 车辆识别码校验算法
    def check_vin(value):
        strs = value.upper()
        if len(strs) != 17:
            return False
        str_to_num = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
            'J': 1,
            'K': 2,
            'L': 3,
            'M': 4,
            'N': 5,
            'P': 7,
            'R': 9,
            'S': 2,
            'T': 3,
            'U': 4,
            'V': 5}
        verify_weight = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
        verify_code = sum([(str_to_num.get(strs[index], 0) if strs[index].isalpha(
        ) else int(strs[index])) * verify_weight[index] for index in range(0, 8)])
        verify_code += sum(
            [(str_to_num.get(strs[index], 0) if strs[index].isalpha() else int(strs[index])
              ) * verify_weight[index] for index in range(9, 17)])
        verify_code = verify_code % 11
        if str(verify_code) == value[8]:
            return True
        else:
            return False


    # 身份证校验算法
    def check_IDNumber(value):
        str_to_int = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                      '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10}
        check_dict = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7',
                      6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
        if len(value) != 18:
            return False

        address = {'11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '34', '35', '36', '37', '41', '42',
                   '43', '44', '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65', '71', '81', '82'}
        if value[:2] not in address:
            return False

        try:
            birth_time = datetime(int(value[6:10]), int(value[10:12]), int(value[12:14]))
            if birth_time >= datetime.now():
                return False
        except:
            return False

        check_num = 0
        for index, num in enumerate(value):
            if index == 17:
                verify_code = check_dict.get(check_num % 11)
                if num == verify_code:
                    return True
                else:
                    return False
            check_num += str_to_int.get(num) * (2 ** (17 - index) % 11)


    # 银行卡校验算法
    def check_bank_card(card_num):
        total = 0
        card_num_length = len(card_num)
        for item in range(1, card_num_length + 1):
            t = int(card_num[card_num_length - item])
            if item % 2 == 0:
                t *= 2
                total += t if t < 10 else t % 10 + t // 10
            else:
                total += t
        return total % 10 == 0


    # findid
    @staticmethod
    def findid(text):
        """
        :param name: id
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Pii.check_IDNumber(text):
            return text
        return None

    # findbankcard
    @staticmethod
    def findbankcard(text):
        """
        :param name: bankcard
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        if Pii.check_bank_card(text):
            return text
        return None


    # findphone
    @staticmethod
    def findphone(text):
        """
        :param name: phone
        :param text: this is a text
        :return: result is a list contain enitty and position
        """
        pattern = r"^[1][345789]\d{9}$"
        ans = re.match(pattern, text)
        if ans:
            return text
        return None

    # findtelephone.
    @staticmethod
    def findtelephone(text):
        """
        :param name: telephone
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        pattern = r"^([0-9]{3,4}-)[0-9]{7,8}$"
        ans = re.match(pattern, text)
        if ans:
            return text
        return None

    # findcarnum
    @staticmethod
    def findcarnum(text):
        """
        :param name: carnum
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        pattern = r"^([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}(([0-9]{5}[DF])|(DF[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})$"
        ans = re.match(pattern, text)
        if ans:
            return text
        return None

    # findemail
    @staticmethod
    def findemail(text):
        """
        :param name: email
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        pattern = r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
        ans = re.match(pattern, text)
        if ans:
            return text
        return None

    # findvin
    @staticmethod
    def findvin(text):
        """
        :param name: vin
        :param text: this is a text
        :return: result is a list contain entity and position
        """
        # pattern = r"^[A-HJ-NPR-Z\d]{8}[\dX][A-HJ-NPR-Z\d]{2}\d{6}$"
        pattern = r"^\b[(A-H|J-N|P|R-Z|0-9)]{17}\b$"
        ans = re.match(pattern, text)
        if ans:
            return text
        return None
