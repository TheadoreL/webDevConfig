#!/usr/bin/env python3

import os
import json
import re
import sys

configPath = sys.path[0]+"/path.conf.json"
confTempPath = sys.path[0]+"/nginx.conf.temp"
confFile = open(configPath)
conf = json.load(confFile)

#write vhohs file via config file
def writeVhosts(appDomain,vhostsConf):
    path = conf['paths']['vhosts'] + "th-conf-" + appDomain + ".conf"
    with open(path,'w') as vhosts:
        vhosts.write(vhostsConf)

#generate vhosts via vhosts templte
def genVhosts(appDomain,appFolder,indexPath):
    serverName = appDomain
    docPath = conf['paths']['wwwRoot']+appFolder+indexPath
    with open(confTempPath,'r') as tempfile:
        tempStr = tempfile.read()
    vhosts = re.compile(r'(\{appPath\})').sub(docPath,re.compile(r'(\{serverName\})').sub(serverName,tempStr))
    print(vhosts)
    def confirm():
        print("please confirm your vhosts y/n (default y)")
        cStr = input()
        if cStr == "y" or cStr == "":
            return True
        elif cStr == "n":
            return False
        else:
            return confirm()
    if confirm():
        return vhosts
    else:
        return False

#restart http server or reload config file
def restartHttp():
    judge = conf['os']+"-"+conf['server']
    if judge == "osx-apache":
        os.system("apachectl restart")
    elif judge == "osx-nginx":
        os.system("brew services restart nginx")
    else:
        print('You should restart your http server')

#append hosts file
def appendHosts(appDomain):
    hostStr = '\n# th-webDevConfig of '+appDomain+'\n127.0.0.1\t'+appDomain
    with open(conf['paths']['hosts'],'a') as hostFile:
        hostFile.write(hostStr)

#get path of app folder
def getAppFolder():
    print("please enter your app folder name:")
    appFolder = input()
    if os.path.exists(conf['paths']['wwwRoot']+appFolder):
        return appFolder
    else:
        print("the path your entered dosn't exists !")
        return getAppFolder()

#get index file path
def getIndexPath():
    keys = []
    print("please choose or enter your index path in your app folder:")
    for key, value in enumerate(conf['indexPath']):
        keys.append(key)
        print("%d -- %s"%(key,value))
    print('enter your path number,\nif your index path doesn\'t in list , enter your index path\nif your index path is your app folder press enter')
    ipath = input()
    def notInList():
        if ipath == "":
            return ""
        else:
            indexPath = re.compile(r'((?:\/\w+)+)').findall(ipath)
            if len(indexPath) > 0:
                indexPath = indexPath[0]
            else:
                print("your enter has some error please enter again!")
                return getIndexPath()
            def confirm():
                print("your index path is %s sure ? y/n (default y)"%(indexPath))
                cStr = input()
                if cStr == "y" or cStr == "":
                    return True
                elif cStr == "n":
                    return False
                else:
                    return confirm()
            if confirm():
                return indexPath
            else:
                return getIndexPath()
    try:
        if int(ipath) in keys:
            indexPath = conf['indexPath'][int(ipath)]
            return indexPath
        else:
            return notInList()
    except:
        return notInList()

#get app's name to generate domain name via config file
def getAppName():
    print("please enter your app name:")
    appName = input()
    fullDomain = appName + conf['domain']
    tmp = '\.'
    reFulld = r''+tmp.join(fullDomain.split('.'))
    def confirm():
        print("your app domain is %s are you sure? y/n (default y)"%(fullDomain))
        cStr = input()
        if cStr == "y" or cStr == "":
            return True
        elif cStr == "n":
            return False
        else:
            return confirm()
    with open(conf['paths']['hosts'],'r') as hostFile:
        hostsStr = hostFile.read()
    if not re.compile(reFulld).search(hostsStr):
        if confirm():
            return fullDomain
        else:
            return getAppName()
    else:
        print("the app name your entered "+fullDomain+" is exist !")
        return getAppName()

print("welcome to web development config tool > <\n")
aFolder = getAppFolder()
fullDomain = getAppName()
indexPath = getIndexPath()
vhosts = genVhosts(fullDomain,aFolder,indexPath)
writeVhosts(fullDomain,vhosts)
appendHosts(fullDomain)
restartHttp()
print("enjoy your development > <")