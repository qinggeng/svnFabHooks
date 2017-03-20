#-*- coding: utf-8 -*-
import settings
import requests, sys, re, os.path
from fabricatorTools.fab import getFab, getUsers
from fabricatorTools.userMock import FabMock

def addTaskComment(**args):
    tid     = args.pop('tid')
    try:
        tid = int(tid)
    except Exception, e:
        tid = int(tid[1:])
    comment = args.pop('comment')
    fab     = args.pop('fab', getFab())

    resp = fab.maniphest.edit(transactions = [{"type": "comment", "value": comment}], objectIdentifier = 'T' + str(tid)).response
    return resp

