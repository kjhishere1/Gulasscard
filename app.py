from getpass import getpass
from urllib.parse import urlparse

from conflib import JsonConfig as Config
from gulasscard import Login, Get, Set, Memorize, Recall


try:
    if type((driver := Login(input(': '), getpass(': ')))) is not str:
        if (driver := Set(input('클래스카드 단어장 주소를 입력하세요.\n: '), driver=driver)) is not None:
            if (key := input('리콜 학습이면 [R], 암기학습이면 [M]을 입력하세요.')) == 'R':
                Recall(input('클래스카드 리콜학습 주소를 입력하세요.\n: '), Get(driver=driver))
            elif key == "M"
                Memorize(input('클래스카드 암기학습 주소를 입력하세요.\n: '), driver=driver)
            else:
                print('정상적인 값이 아닙니다.')
                exit()

except ValueError:
    print('Chrome이 설치되어있지 않습니다.')
    exit()