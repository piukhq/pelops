deliver_data = {
    'mastercard': '<transaction>'
                  '<token>bink_mastercard_token_1</token>'
                  '<state>succeeded</state>'
                  '<succeeded type="boolean">true</succeeded>'
                  '<message>Succeeded!</message>'
                  '<response>'
                  '<headers>      <![CDATA[Content-Type: text/xml]]>    </headers>'
                  '<body>'
                  '<![CDATA[<?xml version="1.0" encoding="UTF-8"?><env:Envelope '
                  'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header '
                  'xmlns:kd4="http://www.ibm.com/KD4Soap" '
                  'xmlns:dat="http://mastercard.com/eis/bnb/servicev1_1/datatypes" '
                  'xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
                  'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">'
                  '<kd4:KD4SoapHeaderV2>PRODESB4_KSC|3891838701|160923075124679</kd4:KD4SoapHeaderV2>'
                  '<dat:bridgeUniqId>PRODESB4_KSC|3891838701|160923075124679</dat:bridgeUniqId>'
                  '</soapenv:Header><env:Body><ns1:doEchoResponse '
                  'xmlns:ns1="http://diagnostic.ws.mcrewards.mastercard.com/">'
                  'Hello Hello</ns1:doEchoResponse></env:Body></env:Envelope>]]>'
                  '</body>'
                  '</response>'
                  '<payment_method>'
                  '<token>WhtIyJrcpcLupNpBD4bSVx3qyY5</token>'
                  '</payment_method>'
                  '</transaction>',
    'amex': '<transaction>'
            '<token>bink_amex_token_1</token>'
            '<state>succeeded</state>'
            '<succeeded type="boolean">true</succeeded>'
            '<message>Succeeded!</message>'
            '<response>'
            '<headers>'
            '<![CDATA[Content-Type: text/xml]]> '
            '</headers> '
            '<body>'
            '<![CDATA[{"status":"Success","respCd":"RCCMP000","respDesc":"Card member successfully enrolled."} ]]>'
            '</body>'
            '</response>'
            '<payment_method>'
            '<token>WhtIyJrcpcLupNpBD4bSVx3qyY5</token>'
            '</payment_method>'
            '</transaction>',
    'visa': {
            "transaction": {
                "response": {
                    "status": 200,
                    "body": """{
    "userDetails": {
        "externalUserId": "a74hd93d9812wir0174mk093dkie1",
        "communityCode": "BINKCTE01",
        "userId": "809902ef-3c0b-40b8-93bf-63e2621df06f",
        "userKey": "a74hd93d9812wir0174mk093dkie1",
        "languageId": "en-US",
        "timeZoneId": "Pacific Standard Time",
        "timeZoneShortCode": "PST",
        "cards": [
            {
                "cardId": "bfc33c1d-d4ef-e111-8d48-001a4bcdeef4",
                "cardLast4": "1111",
                "productId": "A",
                "productIdDescription": "Visa Traditional",
                "productTypeCategory": "Credit",
                "cardStatus": "New"
            }
        ],
        "userStatus": 1,
        "enrollDateTime": "2020-01-29T15:02:55.067"
    },
    "correlationId": "ce708e6a-fd5f-48cc-b9ff-ce518a6fda1a",
    "responseDateTime": "2020-01-29T15:02:55.1860039Z",
    "responseStatus": {
        "code": "SUCCESS",
        "message": "Request proceed successfully without error.",
        "responseStatusDetails": []
    }
}
"""
                    }
                }
            },
    'visa_error': {
            "transaction": {
                "response": {
                    "status": 400,
                    "body": """{
    "userDetails": {
        "externalUserId": "a74hd93d9812wir0174mk093dkie1",
        "communityCode": "BINKCTE01",
        "userId": "809902ef-3c0b-40b8-93bf-63e2621df06f",
        "userKey": "a74hd93d9812wir0174mk093dkie1",
        "languageId": "en-US",
        "timeZoneId": "Pacific Standard Time",
        "timeZoneShortCode": "PST",
        "cards": [
            {
                "cardId": "bfc33c1d-d4ef-e111-8d48-001a4bcdeef4",
                "cardLast4": "1111",
                "productId": "A",
                "productIdDescription": "Visa Traditional",
                "productTypeCategory": "Credit",
                "cardStatus": "New"
            }
        ],
        "userStatus": 1,
        "enrollDateTime": "2020-01-29T15:02:55.067"
    },
    "correlationId": "ce708e6a-fd5f-48cc-b9ff-ce518a6fda1a",
    "responseDateTime": "2020-01-29T15:02:55.1860039Z",
    "responseStatus": {
        "code": "<<error>>",
        "message": "Request proceeded with error.",
        "responseStatusDetails": []
    }
}
"""
                    }
                }
            }
}

export_data = {
    'visa': '{"state": "succeeded", "token": "bink_visa_token_1"}',
}
