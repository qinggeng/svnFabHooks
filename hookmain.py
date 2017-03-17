#!/usr/bin/env python
#-*- coding: utf-8 -*-
import settings
import os, sys
from differential import getDiffRevision

def subcmd(cmd):
    from subprocess import Popen, PIPE
    return Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE).communicate()

def preProcessSvnlookDiff(rawDiff):
    lines = rawDiff.strip()
    lines = filter(lambda x: len(x) > 0, lines.split(u'\n'))
    return u'\n'.join(lines)

def formatDiff(rawDiff):
    from svnDiffParser import Parser
    import re
    fromPattern = re.compile(ur' \(from rev \d+, .*\)$')
    p = Parser()
    p.parse(rawDiff)
    ret = {}
    for (tag, lnum), body in p.ret:
        tag = tag[tag.find(': ') + 2 : -1]
        m = fromPattern.search(tag)
        if None != m:
            tag = tag[: m.start()]
        ret[tag] = body
    return ret

def getReviewDiff(uri):
    from differential import getReviewDifferential
    return getReviewDifferential(uri = uri)

def extractLogArgs(rawLog):
    import re
    p = re.compile(ur'^@([^:]+):(.*)$')
    args = {}
    for line in rawLog.split('\n'):
        m = p.match(line)
        if None != m:
            args[m.groups()[0]] = m.groups()[1]
    return args

def compareDiffs(commitDiff, reviewDiff):
    for f, d in commitDiff.iteritems():
        if f not in reviewDiff:
            print >> sys.stderr, 'commit missing in review request:', f
            return False
        if d != reviewDiff[f]:
            print >> sys.stderr, 'commit content mismatch in review request:', f
            return False
    return True


svnlook = sys.argv[1]
transaction = sys.argv[2]
repo = sys.argv[3]
print >> sys.stderr, "args:", svnlook, transaction, repo
# 从log中抽取review信息
cmd = '{cmd} log -t {txn} "{repo}"'.format(cmd = svnlook, txn = transaction, repo = repo)
cmdout, cmderr = subcmd(cmd)
logArgs = extractLogArgs(cmdout)
try:
    diffUri = logArgs['diffUri'].strip()
except Exception, e:
    print >> sys.stderr, 'commit failed for: missing argument "diffUri" in commit log'
    exit(1)
diffState = getDiffRevision(uri = diffUri)
if diffState['status'] != 'closed':
    print >> sys.stderr, 'commit failed due to this review request is not close'
    exit(1)
reviewDiff = preProcessSvnlookDiff(getReviewDiff(diffUri))
reviewDiff = formatDiff(reviewDiff)
# 获得本次提交的diff
cmd = '{cmd} diff -t {txn} "{repo}"'.format(cmd = svnlook, txn = transaction, repo = repo)
substdout, substderr = subcmd(cmd)
try:
    commitDiff = formatDiff(preProcessSvnlookDiff(substdout))
    ret = compareDiffs(commitDiff, reviewDiff)
    if False == ret:
        exit(1)
    exit(0)
except Exception, e:
    exit(1)
