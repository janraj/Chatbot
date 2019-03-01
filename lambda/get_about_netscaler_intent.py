#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import logging
import json
import bibot_helpers as helpers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.debug('<<Citrix Genie>> Lex event info = ' + json.dumps(event))

    session_attributes = event['sessionAttributes']
    logger.debug('<<Citrix Genie>> lambda_handler: session_attributes = ' + json.dumps(session_attributes))

    return get_about_netscaler_intent_handler(event, session_attributes)

def ns_get_version(ip, username, password):
   resp_version  = requests.get('http://' + ip + '/nitro/v1/config/' + "nsversion", auth=("nsroot", "nsroot"))
   resp_hw = requests.get('http://' + ip + '/nitro/v1/config/' + "nshardware", auth=(username, password))
   list_dict = []
   d = {}
   if "nsversion" in json.loads(resp_version.text):
       out = json.loads(resp_version.text)["nsversion"]
       for key, val in out.items():
          d[key]=val
   list_dict.append(d)
   if "nshardware" in json.loads(resp_hw.text):
      out = json.loads(resp_hw.text)["nshardware"]
      for key, val in out.items():
         e[key]=val
   list_dict.append(e)
   genie_response = list_dict[1]['hwdescription'] + " is running " + list_dict[0]['version'].split(",")[0]
   retun genie_response
    

def get_about_netscaler_intent_handler(intent_request, session_attributes):
    session_attributes['resetCount'] = '0'
    session_attributes['finishedCount'] = '0'
    # don't alter session_attributes['lastIntent'], let Citrix Genie remember the last used intent

    askCount = helpers.increment_counter(session_attributes, 'greetingCount')
   
    genie_response  = ns_get_version("52.91.237.177", "nsroot", "akshata") 
    # build response string
    if askCount == 1: response_string = genie_response
    elif askCount == 2: response_string = genie_response
    else: response_string = 'I have Aleardy told you! Are you kidding me!'

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   

