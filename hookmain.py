#!/usr/bin/env python
#-*- coding: utf-8 -*-
import settings
import os, sys, functools
from differential import getDiffRevision
from osUtils import subcmd
import fabUtils, svnUtils
from fabricatorTools.task import TaskInfoFactory

oldStdout = sys.stdout
sys.stdout = sys.stderr

def validateTasks(logArgs, context):
    try:
        tif     = TaskInfoFactory()
        actions = []
        nextRev = context['youngestRev']() + 1
        author  = context['author']()
        for tid in map(lambda x: x.strip(), logArgs['tasks'].split(',')):
            try:
                tid = int(tid)
            except Exception, e:
                tid = int(tid.strip()[1:])
            task = tif.info(int(tid))
            if True == tif.isClosed(tid):
                print 'commit failed due to task ' + tid + ' alread closed'
                return False
            comment = u'{author} commit at rev{rev} for task {tid}'.format(
                    author = author,
                    rev = nextRev,
                    tid= tid)
            actions.append(functools.partial(fabUtils.addTaskComment, tid = tid, comment = comment))
        for action in actions:
            action()
        return True
            
    except Exception, e:
        print 'commit failed due to missing @tasks in commit log'
        print e
        return False


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
    u"""按文件逐个比较两个diff"""
    for f, d in commitDiff.iteritems():
        if f not in reviewDiff:
            print 'commit missing in review request:', f
            return False
        if d != reviewDiff[f]:
            print 'commit content mismatch in review request:', f
            return False
    return True

svnlook = sys.argv[1]
transaction = sys.argv[2]
repo = sys.argv[3]
context = {}
context['youngestRev'] = functools.partial(svnUtils.youngestRevision, svnlook, repo)
context['author']      = functools.partial(svnUtils.author, svnlook, repo, transaction)
#print "args:", svnlook, transaction, repo
# 从log中抽取review信息
cmd = '{cmd} log -t {txn} "{repo}"'.format(cmd = svnlook, txn = transaction, repo = repo)
cmdout, cmderr, _ = subcmd(cmd)
logArgs = extractLogArgs(cmdout)
#print logArgs
try:
    diffUri = logArgs['diffUri'].strip()
except Exception, e:
    print 'commit failed for: missing argument "diffUri" in commit log'
    exit(1)
diffState = getDiffRevision(uri = diffUri)
if diffState['status'] != 'closed':
    print 'commit failed due to this review request is not close'
    exit(1)
reviewDiff = preProcessSvnlookDiff(getReviewDiff(diffUri))
reviewDiff = formatDiff(reviewDiff)
# 获得本次提交的diff
cmd = '{cmd} diff -t {txn} "{repo}"'.format(cmd = svnlook, txn = transaction, repo = repo)
substdout, substderr, _ = subcmd(cmd)
try:
    commitDiff = formatDiff(preProcessSvnlookDiff(substdout))
    ret = compareDiffs(commitDiff, reviewDiff)
    if False == ret:
        exit(1)
except Exception, e:
    exit(1)
if False == validateTasks(logArgs, context):
    exit(1)

if 'mock' in logArgs:
    exit(1)
exit(0)
