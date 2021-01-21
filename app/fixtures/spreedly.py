deliver_data = {
    "mastercard": "<transaction>"
    "<token>bink_mastercard_token_1</token>"
    "<state>succeeded</state>"
    '<succeeded type="boolean">true</succeeded>'
    "<message>Succeeded!</message>"
    "<response>"
    "<headers>      <![CDATA[Content-Type: text/xml]]>    </headers>"
    "<body>"
    '<![CDATA[<?xml version="1.0" encoding="UTF-8"?><env:Envelope '
    'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header '
    'xmlns:kd4="http://www.ibm.com/KD4Soap" '
    'xmlns:dat="http://mastercard.com/eis/bnb/servicev1_1/datatypes" '
    'xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
    'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">'
    "<kd4:KD4SoapHeaderV2>PRODESB4_KSC|3891838701|160923075124679</kd4:KD4SoapHeaderV2>"
    "<dat:bridgeUniqId>PRODESB4_KSC|3891838701|160923075124679</dat:bridgeUniqId>"
    "</soapenv:Header><env:Body><ns1:doEchoResponse "
    'xmlns:ns1="http://diagnostic.ws.mcrewards.mastercard.com/">'
    "Hello Hello</ns1:doEchoResponse></env:Body></env:Envelope>]]>"
    "</body>"
    "</response>"
    "<payment_method>"
    "<token>WhtIyJrcpcLupNpBD4bSVx3qyY5</token>"
    "</payment_method>"
    "</transaction>",
    "amex": "<transaction>"
    "<token>bink_amex_token_1</token>"
    "<state>succeeded</state>"
    '<succeeded type="boolean">true</succeeded>'
    "<message>Succeeded!</message>"
    "<response>"
    "<headers>"
    "<![CDATA[Content-Type: text/xml]]> "
    "</headers> "
    "<body>"
    '<![CDATA[{"status":"Success","respCd":"RCCMP000","respDesc":"Card member successfully enrolled."} ]]>'
    "</body>"
    "</response>"
    "<payment_method>"
    "<token>WhtIyJrcpcLupNpBD4bSVx3qyY5</token>"
    "</payment_method>"
    "</transaction>",
    "visa": {
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
""",
            }
        }
    },
    "visa_error": {
        "transaction": {
            "token": "JuWy4n4bIlNsgiU3h5yy6Jd4PVi",
            "transaction_type": "DeliverPaymentMethod",
            "state": "failed",
            "created_at": "2020-08-14T15:10:35Z",
            "updated_at": "2020-08-14T15:10:36Z",
            "succeeded": False,
            "message": "Delivery/Export to receiver endpoint returned with an error response code. "
            "Check the transaction transcript for more detail.",
            "url": "https://cert.api.visa.com/vop/v1/users/enroll",
            "response": {
                "status": 400,
                "headers": "Server: nginx\r\nDate: Fri, 14 Aug 2020 15:10:36 GMT\r\n"
                "Content-Type: application/json;charset=utf-8\r\nContent-Length: 293\r\n"
                "Connection: keep-alive\r\nX-SERVED-BY: l73p041\r\n"
                "X-CORRELATION-ID: 1597417835_950_1977034855_l73p041_VDP_WS\r\n"
                "X-Backside-Transport: FAIL FAIL,FAIL FAIL\r\n"
                "Cache-Control: no-cache ,no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\nExpires: -1\r\nX-Powered-By: ASP.NET\r\n"
                "Strict-Transport-Security: max-age=31536000 ,max-age=2592000;includeSubdomains\r\n"
                "X-Global-Transaction-ID: 448482cb5f36a96c87125e09\r\nX-APP-STATUS: 400\r\n"
                "-Frame-Options: SAMEORIGIN\r\nX-XSS-Protection: 1; mode=block\r\n"
                "X-Content-Type-Options: nosniff\r\nX-Cnection: close",
                "body": """
{
    "correlationId":"033440aa-9e91-43ed-8d15-6b27df9ed866",
    "responseDateTime":"2020-08-14T15:10:36.4239243Z",
    "responseStatus":{
        "code":"VALIDATION_FAILED",
        "message":"Request validation failed.",
        "responseStatusDetails":[{
            "code":"<<error>>",
            "message": "User Mocked Error trapped by Pelops"}
        ]}
}
""",
            },
            "receiver": {
                "company_name": "Bink Visa Cert",
                "receiver_type": "bink_visa_cert",
                "token": "7rkxHCRWMFUxbrc4LjLvfBiEHPk",
                "hostnames": "https://cert.api.visa.com/",
                "state": "retained",
                "created_at": "2020-07-23T17:45:54Z",
                "updated_at": "2020-07-23T17:45:54Z",
                "credentials": None,
            },
            "payment_method": {
                "token": "7I8T8A7bcYarl4Fv4oLkLX5XsCo",
                "created_at": "2020-07-24T08:04:19Z",
                "updated_at": "2020-08-14T15:10:28Z",
                "email": None,
                "data": None,
                "storage_state": "retained",
                "test": False,
                "metadata": None,
                "callback_url": None,
                "last_four_digits": "7103",
                "first_six_digits": "424242",
                "card_type": "visa",
                "first_name": "Mart Staging",
                "last_name": "Test",
                "month": 6,
                "year": 2022,
                "address1": None,
                "address2": None,
                "city": None,
                "state": None,
                "zip": None,
                "country": None,
                "phone_number": None,
                "company": None,
                "full_name": "Mart Staging Test",
                "eligible_for_card_updater": True,
                "shipping_address1": None,
                "shipping_address2": None,
                "shipping_city": None,
                "shipping_state": None,
                "shipping_zip": None,
                "shipping_country": None,
                "shipping_phone_number": None,
                "payment_method_type": "credit_card",
                "errors": [],
                "fingerprint": "063fcf0319dcd8ac014867ee0919495276c6",
                "verification_value": "",
                "number": "XXXX-XXXX-XXXX-7103",
            },
        }
    },
}

export_data = {
    "visa": '{"state": "succeeded", "token": "bink_visa_token_1"}',
}
