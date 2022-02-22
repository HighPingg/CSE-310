import dns.message
import dns.query
import dns.rrset

ROOT_SERVERS = ['198.41.0.4',
               '199.9.14.201',
               '192.33.4.12',
               '199.7.91.13',
               '192.203.230.10',
               '192.5.5.241',
               '192.112.36.4',
               '198.97.190.53',
               '192.36.148.17',
               '192.58.128.30',
               '193.0.14.129',
               '199.7.83.42',
               '202.12.27.33'
               ]

def mydig(domain: str):
    printMessage(queryRoot(domain))


def queryRoot(domain: str) -> dns.message.Message:

    # Make the name object and the request.
    domain = dns.name.from_text(domain)
    request = dns.message.make_query(domain, dns.rdatatype.A)

    # Loop through the root servers and query them until we
    # find one that returns a correct answer.

    for rootServer in ROOT_SERVERS:
        answer = queryServer(request, rootServer)

        # If we have a valid answer, we can terminate the root
        # server request loop.
        if len(answer.answer) != 0:
            # If the name was a CNAME, we have to re-dig that name
            # (I only resolve the first one)
            if 'CNAME' in answer.to_text():
                answer = queryRoot(answer.answer[0].to_text().split(' ')[-1])

            return answer
    
    return None
            
    
def queryServer(request, server):
    """Recursively resolves a given Message at a given server.

    *request*, the Message type that we want to query.

    *server*, the server that we want to query.
    
    Returns the server answer Message if successful.
    """
    # Request the server
    response = dns.query.udp(request, server)

    # If this resulted in answer, we can return it.
    if len(response.answer) != 0:
        return response

    # We then want to check our additional and authoritative fields
    # and then loop through those until we have a valid answer.
    for i in range(len(response.additional)):
        # Check if it's ipv6. If it is, then we ignore it.
        if ':' not in str(response.additional[i][0]):
            answer = queryServer(request, str(response.additional[i][0]))

            # If we have an answer, we return it
            if len(answer.answer) != 0:
                return answer
    
    # If the additional servers didnt return anything, then we can query
    # the authority servers.

    for i in range(len(response.authority)):
        # Only resolve NS records
        if ' IN NS ' in response.authority[i].to_text():
            answer = queryRoot(response.authority[i].to_text().split(' ')[-1])

        # If we have an answer, we return it
        if len(answer.answer) != 0:
            return answer

    # Otherwise, we found nothing and we just return None
    return None

def printMessage(answer):

    # Print question section
    print('QUESTION SECTION:')
    for question in answer.question:
        print(question)

    # Newline
    print()

    # Print answer section
    print('ANSWER SECTION:')
    for answer in answer.answer:
        print(answer)

    # Newline
    print()
