# MyDig

`mydig()` is a function written in python that allows you to resolve a name to an IP
through one function call.

## Dependencies

The [dnspython](https://www.dnspython.org/) package is required to run MyDig. It can
be installed through [pip](https://pip.pypa.io/en/stable/), using the command:

```bash
pip install dnspython
```

A version of Python 3 that's compatible with dnspython must also be installed.

## Usage

To use MyDig, you first need to import it. `mydig()` takes in a domain and prints out
a canonicalized output according to the one inside the doc.

```python
>>> from mydig import mydig
>>> mydig('amazon.com')
QUESTION SECTION:
amazon.com. IN A

ANSWER SECTION:
amazon.com. 60 IN A 205.251.242.103
amazon.com. 60 IN A 54.239.28.85
amazon.com. 60 IN A 176.32.103.205

Query time: 130 ms
WHEN: 19:08:36 02/22/2022
```
You can also directly get the final response message from the last name server that mapped the name to the IP by calling the `queryRoot()` method. It takes a a string as
an argument which is the domain you want to resolve. An example can be seen below: *(This wasn't in the instructions so plz don't deduct points for it ty :) )*

```python
>>> from mydig import queryRoot
>>> print(queryRoot('amazon.com'))
id 49968
opcode QUERY
rcode NOERROR
flags QR AA RD
;QUESTION
amazon.com. IN A
;ANSWER
amazon.com. 60 IN A 176.32.103.205
amazon.com. 60 IN A 205.251.242.103
amazon.com. 60 IN A 54.239.28.85
;AUTHORITY
;ADDITIONAL
```
