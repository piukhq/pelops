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
            '</transaction>'
}

export_data = {
    'visa': '{"state": "succeeded", "token": "bink_visa_token_1"}',
}
