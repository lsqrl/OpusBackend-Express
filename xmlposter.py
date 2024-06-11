import urllib.parse
import urllib.request

# urlparse

import base64
import argparse
import sys

 

class Xmlposter(object):

    def __init__(self, host='18.159.213.75', port='8500',

                 username='feeuser',

                 password='password1',

                 *args, **kwargs):

        self.host = host

        self.port = port

        self.username = username
        self.password = password

 

        user_password_str = '%s:%s' % (username, password)

        self.base64string = base64.b64encode(user_password_str.encode())
        
        self.url = 'http://%s:%s/pricing/xmlposter' % (host, port)

        self.xml_output = None

 

 

    def request(self, currency, ctrCcy, strategy, maturity, strike):
        data =  urllib.parse.urlencode({'xml': f"""<?xml version="1.0" encoding="UTF-8"?>
                <gfi_message version="2.0">
                <header>
                    <transactionId>1234567890</transactionId>
                    <timestamp>2006-03-06T15:55:22-05:00</timestamp>
                    <username>feeuser</username>
                    <password>password1</password>
                </header>
                <body>
                    <action name="action1" function="PRICING" version="1.0">
                        <option name="calc" value="MIDRATE"/>
                        <option name="data" ref="data1"/>
                        <option name="scenario" value="Trading"/>
                    </action>
                    <data name="data1" format="NAME_VALUE">
                        <node name="1">
                            <field name="Class" value="European"/>
                            <field name="Currency" value="{currency}"/>
                            <field name="CtrCcy" value="{ctrCcy}"/>
                            <field name="Strategy" value="{strategy}"/>
                            <field name="Maturity" value="{maturity}"/>
                            <field name="Strike" value="{strike}"/>
                        </node>
                    </data>
                </body>
                </gfi_message>"""})

        binary_data = data.encode('utf-8')

        headers = {'Content-Type': "application/x-www-form-urlencoded",

           'Content-Length': len(data),

           'Authorization': 'Basic %s' % self.base64string}

 

        req = urllib.request.Request(url=self.url,

                                data = binary_data,

                                headers=headers)

 

        try:

            response = urllib.request.urlopen(req, timeout=60)

            self.xml_output = response.read().decode("utf-8")

 

        except urllib.error.HTTPError as e:

            print('There was an error with the request')

            print(e)

            print(e.headers)

            print(e.headers.has_key('WWW-Authenticate'))

 

        return self.xml_output


def main():
    poster = Xmlposter()

    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--currency', type=str, required=True, help='Specify the currency')
    parser.add_argument('--ctrCcy', type=str, required=True, help='Specify the control currency')
    parser.add_argument('--maturity', type=str, required=True, help='Specify the maturity')
    parser.add_argument('--strike', type=str, required=True, help='Specify the strike')
    parser.add_argument('--strategy', type=str, required=True, choices=['call', 'put'], help='Specify the strategy (either "call" or "put")')
    
    args = parser.parse_args()
    # Call the request function with the parsed arguments
    result = poster.request(args.currency, args.ctrCcy, args.strategy, args.maturity, args.strike)
    print(result);

if __name__ == '__main__':
    main()