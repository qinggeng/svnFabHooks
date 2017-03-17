#-*-coding: utf-8 -*-
kWorkingcopyPath = u""
import os.path
def regularCommit():
    u"""test regular commit process
= PROCESS
# append random content to some local files
# create new random local files and added them to svn
# delete some local files randomly
# generate review request
# approve review
# commit
= EXPACTED RESULT
# commit success
"""
    # randomly create 2 local files
    content = datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
    os.system('echo "%s" >> %s' % (content, os.path.join(kWorkingcopyPath, "test")))
