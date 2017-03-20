#-*- coding: utf-8 -*-

import osUtils

def youngestRevision(svnlook, repo):
    cmd = u'"{svnlook}" youngest "{repo}"'.format(svnlook = svnlook, repo = repo)
    subout, suberr, retcode = osUtils.subcmd(cmd)
    if 0 != retcode:
        raise RuntimeError("get next revision number in repository failed, cmd: " + cmd)
    return int(subout.strip())

def author(svnlook, repo, txn):
    cmd = u'"{svnlook}" author "{repo}" -t "{txn}"'.format(
            svnlook = svnlook,
            repo = repo,
            txn = txn)
    subout, suberr, retcode = osUtils.subcmd(cmd)
    if 0 != retcode:
        raise RuntimeError("get author failed, cmd: " + cmd)
    authorName = subout.strip()
    if len(authorName) == 0:
        authorName = 'Anonymous'
    return authorName
