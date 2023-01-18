import requests
import json
from pprint import pprint

with open("config.json","r") as f:
    config = json.load(f)
with open("events.json","r") as f:
    reports = json.load(f)

def get_event(event_id: str =""):
    if event_id:
        try:
            r = requests.get(f"https://api.tidyhq.com/v1/events/{event_id}",params={"access_token":config["tidytoken"]})
            if r.status_code == 200:
                event = r.json()
                return event
            print(r.status_code)
            print(r.text)
            return False
        except requests.exceptions.RequestException as e:
            print(e)
            return False

def get_tickets(event_id: str =""):
    if event_id:
        try:
            r = requests.get(f"https://api.tidyhq.com/v1/events/{event_id}/tickets/",params={"access_token":config["tidytoken"]})
            if r.status_code == 200:
                tickets = r.json()
                return tickets
            print(r.status_code)
            print(r.body)
            return False
        except requests.exceptions.RequestException as e:
            print(e)
            return False

for report in reports:
    lines = """"""
    for event in reports[report]:
        e = get_event(event_id=event)
        if e:
            #print(f'{e["name"]} - {(e["start_at"])}')
            tickets = get_tickets(event_id=event)
            total = 0
            tlines = """"""
            for ticket in tickets:
                total += ticket["quantity_sold"] * float(ticket["amount"])
                #print(f'{ticket["name"]} - {ticket["quantity_sold"]} tickets (${ticket["quantity_sold"] * ticket["amount"]})')
                tlines += f'<li>{ticket["name"]}: {ticket["quantity_sold"]}</li>\n'
            lines += f"""<tr>
        <td>{e["name"]}</td>
        <td>{e["start_at"]}</td>
        <td><ul>{tlines}</ul></td>
        <td>${total}</td>
      </tr>"""
        
        else:
            print("heh")
    with open("template.html","r") as t:
        template = t.read()
        with open(f"generated/{report}.html","w") as f:
            f.write(template.format(lines))

    #print(lines)
