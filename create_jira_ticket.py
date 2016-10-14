#!/usr/bin/python3.4
import webbrowser as wb
import sys
import json
from restkit import BasicAuth, Resource
__author__ = 'Daniel Pasacrita'
__date__ = '10/6/16'


def create_ticket(host_url, auth, ticket_fields):
    """
    Takes all of the necessary information about the server and ticket and submits a POST request
    to the jira server's Rest API to create a ticket.

    :param host_url: The url of the jira server.
    :param auth: Credentials to the account the ticket will be created as.
    :param ticket_fields: a dictionary containing all of the information/data necessary to create the ticket

    :return: jira_issue: The json of the response from the server. This can be used to get information about the created
    ticekt later on.
    """

    # Constructing the URL to POST to
    complete_url = "%s/rest/api/2/issue/" % host_url
    # Create the resource using restkit
    resource = Resource(complete_url, filters=[auth])
    post_headers = {'Content-Type': 'application/json'}

    # Try POSTing to Jira Rest API. If failure, exit and print error message.
    try:
        data = {
            "fields": {
                "project": {
                    "key": ticket_fields['project']
                },
                "summary": ticket_fields['summary'],
                "issuetype": {
                    "name": ticket_fields['issue_type']
                }
            }
        }
        response = resource.post(headers=post_headers, payload=json.dumps(data))
    except Exception, ex:
        print("EXCEPTION: %s " % ex.message)
        return None

    if response.status_int / 100 != 2:
        print "ERROR: status %s" % response.status_int
        return None

    # Gather the json from the response into an array
    jira_issue = json.loads(response.body_string())

    return jira_issue


def set_ticket_data():
    """
    This function will allow the user to enter via the command line what fields and information he wants
    in the ticket.

    :return: ticket_data: A dictionary containing all the entered data for the ticket
    """
    # Create dictionary
    ticket_data = dict()

    # Accept input from user for all aspects
    ticket_data['project'] = raw_input("Please enter Project Key")
    ticket_data['issue_type'] = raw_input("Please enter Issue Type")
    ticket_data['summary'] = raw_input("Please enter Ticket summary")

    return ticket_data

if __name__ == "__main__":

    # testing variable - if true, skip everything except the code up here.
    testing = 0
    if testing is 1:
        set_ticket_data()
        sys.exit(0)

    # Jira Server information and credentials
    server_url = "http://jira.domain.com"
    jira_auth = BasicAuth("user", "password")

    # Set Jira ticket information
    ticket_info = set_ticket_data()

    # Call create_ticket, which returns the ticket info in an array.
    issue = create_ticket(server_url, jira_auth, ticket_info)
    issue_code = issue["key"]
    issue_url = "%s/browse/%s" % (server_url, issue_code)

    # Open the ticket in the default web browser, assuming it created correctly.
    if issue is not None:
        print(issue)
        wb.open(issue_url)
    else:
        sys.exit(2)
