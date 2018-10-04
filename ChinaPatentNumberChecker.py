#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date


def checkpatnum(patnum, withdot = False):
    """
    判断 patnum 是正确的专利号，
    专利号前可以带有CN或ZL，也不可不带，不影响校验结果：
    专利号校验位前可以有"."，也可以没有，不影响校验结果：
    正确则根据参数 withdot 的值返回相应的带点或不带点的专利号；
    不正确则返回 False 。
    基本判断流程：
    统一去除"."；
    校验位改为大写；
    去除专利号头部的CN或者ZL前缀；
    判断除最后一位校验位外是否全部为数字；
    判断校验位是否为数字或者X；
    判断位数是否为9或者13，规范专利号；
    判断年份信息是否正确；
    判断类型位是否为1、2、3、8、9；
    判断校验位是否正确；
    """
    patnum = patnum.replace('.', "")
    patnum = patnum.upper()
    if patnum.startswith("CN") or patnum.startswith("ZL"):
        #去除专利号头部的CN或ZL前缀
        patnum = patnum[2:]

    if not (patnum[:-1].isdigit() and patnum[-1] in "0123456789X"):
        return False

    lengthofpatnum = len(patnum)
    if lengthofpatnum == 9:
        year, typenumber= int(patnum[:2]), patnum[2]
        year += 1900 if year >= 85 else 2000
        if not 1985 <= year <= 2003:
            return False
        #10位的专利号只在85年专利法开始实施到2003年在使用。
    elif lengthofpatnum == 13:
        year, typenumber= int(patnum[:4]), patnum[4]
        if not 2003 <= year <= date.today().year:
            return False
        #14位的专利号只在2003年以后使用。
    else:
        return False

    if typenumber not in "12389":
        return False

    tempx = "23456789" if lengthofpatnum == 10 else "234567892345"
    if "0123456789X"[sum(int(d) * int(p) for d, p in zip(patnum[:-1], tempx)) % 11] == patnum[-1]:
        if withdot:
            return patnum[:-1] + '.' + patnum[-1]
        else:
            return patnum
    else:
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("patnum",help="China Patent Number.")
    parser.add_argument("--withdot", help="Whether the output China patent number with a dot or not.", action="store_true")
    args = parser.parse_args()
    print(checkpatnum(args.patnum, args.withdot))
