import urllib.request as urllib2
import base64
import ssl
import json
import csv
import sys, getopt

cfg = {'jira_host_address': 'https://www.jira.com/jira',
       'jira_username': 'my_username',
       'jira_user_password': 'password_string',
       'max_results': '1000',
       'jira_project': 'MAD17'
       }

context = ssl._create_unverified_context()
myWorklogs = []


def getAllIssueIds():
    allIssuesUrl = cfg['jira_host_address'] + '/rest/api/2/search?jql=project=' + cfg['jira_project'] + '&maxResults=' + \
                   cfg['max_results']

    issues = getRequestWithAuthHeaderRetJson(allIssuesUrl)['issues']
    issueIds = []

    for issue in issues:
        issueIds.append(issue['key'])

    return issueIds


def getWorklogForIssue(key):
    issueWorklogUrl = cfg['jira_host_address'] + '/rest/api/2/issue/' + key + '/worklog'
    worklogsJson = getRequestWithAuthHeaderRetJson(issueWorklogUrl)

    worklogs = worklogsJson['worklogs']

    for worklog in worklogs:
        new_work_log = []
        author = worklog['author']['name']
        timeSpent = worklog['timeSpentSeconds']

        new_work_log.append(author)
        new_work_log.append(key)
        new_work_log.append(timeSpent)
        myWorklogs.append(new_work_log)

    return myWorklogs


def getRequestWithAuthHeaderRetJson(requestUrl):
    request = urllib2.Request(requestUrl)
    sUserPw = '%s:%s' % (cfg['jira_username'], cfg['jira_user_password'])
    base64string = base64.b64encode(str.encode(sUserPw))
    request.add_header("Authorization", b'Basic ' + base64string)
    result = urllib2.urlopen(request, context=context)
    respJson = result.read()
    jsonData = json.loads(respJson)
    return jsonData


def getAllUsers():
    userDict = {}

    for worklog in myWorklogs:
        user = worklog[0]
        userDict[user] = user

    userArr = []
    for key in userDict:
        userArr.append(key)

    return userArr


def getOverallWorklogByUser():
    users = getAllUsers()

    user_summary_file = open('time_report_summary.txt', 'wt', encoding="UTF-8")

    for user in users:
        userTimeSeconds = 0
        for worklog in myWorklogs:
            if (worklog[0] == user):
                userTimeSeconds += worklog[2]


        print(user + ' spent ' + str(userTimeSeconds) + ' seconds on the project')
        s_user_time = user + ' spent ' + str(userTimeSeconds / 3600) + ' hours on the project'
        print(s_user_time + '\n')
        user_summary_file.write(s_user_time + '\n')

    user_summary_file.close()

def readCommandLine(args):

    opts,args = getopt.getopt(args, 'h:u:p:')

    for opt, arg in opts:
        if opt == '-h':
            cfg['jira_host_address'] = arg
        elif opt == '-u':
            cfg['jira_username'] = arg
        elif opt == '-p':
            cfg['jira_user_password'] = arg

def main():

    print("to use this script u can either change cfg dict in the script file or use the following command line options")
    print("-h <host - z.B. https://www.myjira.de -u <username of your jira user> -p <password of your jira user> \n\n")
    readCommandLine(sys.argv[1:])

    allIssueIds = getAllIssueIds()

    for issueId in allIssueIds:
        getWorklogForIssue(issueId)

    print(myWorklogs)


    with open('time_report.csv', 'wt', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for worklog in myWorklogs:
            if len(worklog) > 0:
                writer.writerow(worklog)

    getOverallWorklogByUser()

    return 0


main()
