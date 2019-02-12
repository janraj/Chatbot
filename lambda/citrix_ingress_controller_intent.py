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

    return citrix_ingress_controller_intent_handler(event, session_attributes)


def citrix_ingress_controller_intent_handler(intent_request, session_attributes):
    session_attributes['resetCount'] = '0'
    session_attributes['finishedCount'] = '0'
    # don't alter session_attributes['lastIntent'], let Citrix Genie remember the last used intent

    askCount = helpers.increment_counter(session_attributes, 'greetingCount')
    
    # build response string
    if askCount == 1: response_string = "Citrix Genie at your service! How can I help?"
    elif askCount == 2: response_string = "Genie here"
    elif askCount == 3: response_string = "Genie listening"
    elif askCount == 4: response_string = "Yes?"
    elif askCount == 5: response_string = "Really?"
    elif askCount == 6: response_string = "Please refer here for more details about Citrix Ingress controller\n https://github.com/citrix/citrix-k8s-ingress-controller"
    else: response_string = 'Ok'

    return helpers.close(session_attributes, 'Fulfilled', {'contentType': 'PlainText','content': response_string})   

