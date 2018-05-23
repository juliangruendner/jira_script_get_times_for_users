# jira_script_get_times_for_users

this script will generate a csv (time_report.csv) file with the times each user spend on each task on a project.

It will also generate a summary (time_report_summary.txt, which includes the times a user has spend on a project overall.


call the script as follows:


python3 getReport.py -h <host - z.B. https://www.myjira.de -u <username of your jira user> -p <password of your jira user> -g <project used>
please note that: 
1. the pw has to be in '' if it contains for example a #
2. your user needs to have the required access permissions in order for this script to work.