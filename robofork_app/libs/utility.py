"""
Utility関数群
"""


def to_hex(value, padding_count=4):
    """
    数値を16進数文字列へ変換する
    :param value: 変換対象数値
    :param padding_count: 16新文字列の桁数
    :return:
    """
    return hex(value).split('x')[-1].zfill(padding_count)


def to_can_data(value):
    """
    CAN通信向けの文字列に変更する
    :param value: 16進数文字列（012A4Cなど）
    :return:
    """
    return [(i + j) for (i, j) in zip(value[::2], value[1::2])]
