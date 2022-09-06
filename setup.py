#!/usr/bin/env python
#
#

target = "boty" # BHJTW change this to /var/cache/jsb on debian

import os

try: from setuptools import setup
except: print "i need setuptools to properly install BOTY" ; os._exit(1)

upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir): print "%s does not exist" % dir ; os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc"):
                continue
            upl.append(d)

    return upl

setup(
    name='boty',
    version='0.1.1',
    url='http://boty.googlecode.com/',
    download_url="http://code.google.com/p/boty/downloads", 
    author='Bart Thate',
    author_email='bthate@gmail.com',
    description='Time Flies',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/boty',
             'bin/boty-xmpp'],
    packages = [ 'boty',
                 'boty/drivers',
                 'boty/drivers/xmpp',
                 'boty/lib',
                 'boty/plugs',
                 'boty/contrib/',
                 'boty/contrib/sleekxmpp',
                 'boty/contrib/sleekxmpp/stanza',   
                 'boty/contrib/sleekxmpp/test',     
                 'boty/contrib/sleekxmpp/roster',   
                 'boty/contrib/sleekxmpp/xmlstream',
                 'boty/contrib/sleekxmpp/xmlstream/matcher',
                 'boty/contrib/sleekxmpp/xmlstream/handler',
                 'boty/contrib/sleekxmpp/plugins',
                 'boty/contrib/sleekxmpp/plugins/xep_0004',
                 'boty/contrib/sleekxmpp/plugins/xep_0004/stanza',
                 'boty/contrib/sleekxmpp/plugins/xep_0009',
                 'boty/contrib/sleekxmpp/plugins/xep_0009/stanza',
                 'boty/contrib/sleekxmpp/plugins/xep_0030',
                 'boty/contrib/sleekxmpp/plugins/xep_0030/stanza',
                 'boty/contrib/sleekxmpp/plugins/xep_0050',
                 'boty/contrib/sleekxmpp/plugins/xep_0059',
                 'boty/contrib/sleekxmpp/plugins/xep_0060',
                 'boty/contrib/sleekxmpp/plugins/xep_0060/stanza',
                 'boty/contrib/sleekxmpp/plugins/xep_0066',
                 'boty/contrib/sleekxmpp/plugins/xep_0078',
                 'boty/contrib/sleekxmpp/plugins/xep_0085',
                 'boty/contrib/sleekxmpp/plugins/xep_0086',
                 'boty/contrib/sleekxmpp/plugins/xep_0092',
                 'boty/contrib/sleekxmpp/plugins/xep_0128',
                 'boty/contrib/sleekxmpp/plugins/xep_0199',
                 'boty/contrib/sleekxmpp/plugins/xep_0202',
                 'boty/contrib/sleekxmpp/plugins/xep_0203',
                 'boty/contrib/sleekxmpp/plugins/xep_0224',
                 'boty/contrib/sleekxmpp/plugins/xep_0249',
                 'boty/contrib/sleekxmpp/features',
                 'boty/contrib/sleekxmpp/features/feature_mechanisms',
                 'boty/contrib/sleekxmpp/features/feature_mechanisms/stanza',
                 'boty/contrib/sleekxmpp/features/feature_starttls',
                 'boty/contrib/sleekxmpp/features/feature_bind',   
                 'boty/contrib/sleekxmpp/features/feature_session',
                 'boty/contrib/sleekxmpp/thirdparty',
                 'boty/contrib/sleekxmpp/thirdparty/suelta',
                 'boty/contrib/sleekxmpp/thirdparty/suelta/mechanisms',
                 ],
    long_description = """ -=- always wanted to be a bird -=- """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    requires=['jsb', 
               'dnspython'
             ]
)
