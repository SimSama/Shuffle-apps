import time
import json
import json
import random
import socket
import asyncio
import requests

class HTTP(AppBase):
    __version__ = "1.0.0"
    app_name = "secureworks"  

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def get_ticket_ids(self, username, password, tickettype="", groupingtype="", limit="10"):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/ids" 
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        params = {
            "limit": limit,
        }
    
        if tickettype:
            params["ticketType"] = tickettype
        if groupingtype:
            params["groupingType"] = groupingtype 
    
        # Might need body?
        ret = requests.post(url, params=params, headers=headers)
        return ret.text
    
    async def get_ticket(self, username, password, ticketId, includeWorklogs=False):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/%s" % (ticketId)
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        params = {
            "includeWorklogs": includeWorklogs,
        }
    
        # Might need body?
        ret = requests.get(url, params=params, headers=headers)
        return ret.text
    
    async def close_ticket(self, username, password, ticketId, closeCode, worklogContent):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/%s/close" % (ticketId)
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        data = {
            "worklogContent": worklogContent,
            "closeCode": closeCode,
        }
    
        # Might need body?
        ret = requests.post(url, headers=headers, json=data)
        return ret.text
    
    async def add_worklog(self, username, password, ticketId, body):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/%s/worklogs" % (ticketId)
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        data = {
            "content": body,
        }
    
        # Might need body?
        ret = requests.post(url, headers=headers, json=data)
        return ret.text
    
    async def assign_ticket(self, username, password, ticketId, body):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/%s/assign" % (ticketId)
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        data = {
            "worklog": body,
        }
    
        # Might need body?
        ret = requests.post(url, headers=headers, json=data)
        return ret.text
    
    # Supposed to take multiple, but can be looped outside instead (:
    async def acknowledge_ticket(self, username, password, ticketId, version):
        url = "https://api.secureworks.com/api/ticket/v3/tickets/acknowledge" 
        headers = {
            "Authorization": "APIKEY %s:%s" % (username, password),
            "Content-Type": "application/json",
        }
    
        # ticketype, limit, groupingType
        data = {
            "ticketVersions": [{
                "ticketId": ticketId,
                "version": version,
            }],
        }
    
        # Might need body?
        ret = requests.post(url, headers=headers, json=data)
        return ret.text

# Run the actual thing after we've checked params
def run(request):
    action = request.get_json() 
    print(action)
    print(type(action))
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")
	
    if action and "name" in action and "app_name" in action:
        asyncio.run(HTTP.run(action), debug=True)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}' 
    else:
        return f'Invalid action'

	