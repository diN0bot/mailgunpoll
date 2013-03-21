import settings

def via_pop():
    import poplib

    for mailbox_cred in settings.MAILBOX_CREDS:
        mailbox = poplib.POP3(settings.POP3DOMAIN)
        mailbox.user(mailbox_cred['user']+'@'+settings.MAILBOX_DOMAIN)
        mailbox.pass_(mailbox_cred['pass'])
        msg, _, _ = mailbox.list()
        print "%s has %s votes" % (mailbox_cred['user'], msg.split()[1])

def via_logs():
    import requests
    import re
    url = 'https://api.mailgun.net/v2/'+settings.MAILBOX_DOMAIN+'/log'
    response = requests.get(url, auth=('api', settings.API_KEY))
    # {'yes': {'email':1, ...}, }
    visited = {}
    # {'yes': 22, ...}
    counts = {}
    for item in response.json()['items']:
        from_email = re.match('Received:  (\S+) ', item['message']).group(1)
        for_vote = re.search(' (\w+)+@'+settings.MAILBOX_DOMAIN, item['message']).group(1)
        if not for_vote in visited:
            visited[for_vote] = {}
        if not from_email in visited[for_vote]:
            visited[for_vote][from_email] = 1
            if not for_vote in counts:
                counts[for_vote] = 0
            counts[for_vote] += 1
    print counts

if __name__ == '__main__':
    via_pop()
    print
    print "-"*80
    print
    via_logs()
