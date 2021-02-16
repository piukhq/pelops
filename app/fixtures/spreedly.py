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
    "amex": """<transaction>
  <token>DhZzjauzqnSTXyhVx0ylmEJTV44</token>
  <transaction_type>DeliverPaymentMethod</transaction_type>
  <state>succeeded</state>
  <created_at type="dateTime">2021-02-16T00:26:10Z</created_at>
  <updated_at type="dateTime">2021-02-16T00:26:11Z</updated_at>
  <succeeded type="boolean">true</succeeded>
  <message>Succeeded!</message>
  <url>https://api.dev2s.americanexpress.com/marketing/v4/smartoffers/card_accounts/cards/sync_details</url>
  <response>
    <status type="integer">200</status>
    <headers>
      <![CDATA[Date: Tue, 16 Feb 2021 00:26:11 GMT
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Server: Apache-Coyote/1.1]]>
    </headers>
    <body>
      <![CDATA[{"correlationId":"1613435163",
      "status":"Success","respCd":"RCCMP000","respDesc":"Card member successfully enrolled.",
      "cmAlias1":"QdjGCPSiYYDKxPMvvluYRG6zq79"}]]>
    </body>
  </response>
  <receiver>
    <company_name>American Express</company_name>
    <receiver_type>american_express</receiver_type>
    <token>TmOF7n6qdXkCC3lErt1ThRdXsAW</token>
    <hostnames>https://api.qa.americanexpress.com, https://api.americanexpress.com, https://www206.americanexpress.com,
     https://fsgateway.aexp.com, sftp://fsgateway.aexp.com, https://apigateway2s.americanexpress.com,
      https://api.qa2s.americanexpress.com, https://api.dev2s.americanexpress.com, 
      https://apisl.americanexpress.com, https://sandbox.americanexpress.com, https://www396.americanexpress.com, 
      https://api-test.americanexpress.com, https://api2s.americanexpress.com, 
      https://apigateway.americanexpress.com</hostnames>
    <state>retained</state>
    <created_at type="dateTime">2021-02-02T17:54:23Z</created_at>
    <updated_at type="dateTime">2021-02-02T17:54:23Z</updated_at>
    <credentials type="array">
      <credential>
        <name>app-id</name>
        <value type="integer">1234</value>
        <safe type="boolean">true</safe>
      </credential>
      <credential>
        <name>app-secret</name>
        <safe>false</safe>
      </credential>
    </credentials>
  </receiver>
  <payment_method>
    <token>QdjGCPSiYYDKxPMvvluYRG6zq79</token>
    <created_at type="dateTime">2021-02-02T19:54:55Z</created_at>
    <updated_at type="dateTime">2021-02-16T00:26:11Z</updated_at>
    <email>joey@example.com</email>
    <data nil="true"/>
    <storage_state>retained</storage_state>
    <test type="boolean">true</test>
    <metadata>
      <key>string value</key>
      <another_key type="integer">123</another_key>
      <final_key type="boolean">true</final_key>
    </metadata>
    <callback_url nil="true"/>
    <last_four_digits>0005</last_four_digits>
    <first_six_digits>378282</first_six_digits>
    <card_type>american_express</card_type>
    <first_name>Joe</first_name>
    <last_name>Jones</last_name>
    <month type="integer">3</month>
    <year type="integer">2032</year>
    <address1>33 Lane Road</address1>
    <address2>Apartment 4</address2>
    <city>Wanaque</city>
    <state>NJ</state>
    <zip>31331</zip>
    <country>US</country>
    <phone_number>919.331.3313</phone_number>
    <company>Acme Inc.</company>
    <full_name>Joe Jones</full_name>
    <eligible_for_card_updater type="boolean">true</eligible_for_card_updater>
    <shipping_address1>33 Lane Road</shipping_address1>
    <shipping_address2>Apartment 4</shipping_address2>
    <shipping_city>Wanaque</shipping_city>
    <shipping_state>NJ</shipping_state>
    <shipping_zip>31331</shipping_zip>
    <shipping_country>US</shipping_country>
    <shipping_phone_number>919.331.3313</shipping_phone_number>
    <payment_method_type>credit_card</payment_method_type>
    <errors>
    </errors>
    <verification_value></verification_value>
    <number>XXXX-XXXX-XXXX-0005</number>
    <fingerprint>3b71a994ea0b417babcab7111af5757d3ea8</fingerprint>
  </payment_method>
</transaction>
""",
    "amex_error": """<transaction>
  <token>S2Qrz7pqhw8x0soEPGDqC0vlE14</token>
  <transaction_type>DeliverPaymentMethod</transaction_type>
  <state>succeeded</state>
  <created_at type="dateTime">2021-02-16T00:44:03Z</created_at>
  <updated_at type="dateTime">2021-02-16T00:44:03Z</updated_at>
  <succeeded type="boolean">true</succeeded>
  <message>Succeeded!</message>
  <url>https://api.dev2s.americanexpress.com/marketing/v4/smartoffers/card_accounts/cards/sync_details</url>
  <response>
    <status type="integer">200</status>
    <headers>
      <![CDATA[Date: Tue, 16 Feb 2021 00:44:03 GMT
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Server: Apache-Coyote/1.1]]>
    </headers>
    <body>
      <![CDATA[{"correlationId":"1613436239",
      "status":"Failure","respCd":"<<error>>","respDesc":"Mocked error from Pelops",
      "cmAlias1":"QdjGCPSiYYDKxPMvvluYRG6zq79"}]]>
    </body>
  </response>
  <receiver>
    <company_name>American Express</company_name>
    <receiver_type>american_express</receiver_type>
    <token>TmOF7n6qdXkCC3lErt1ThRdXsAW</token>
    <hostnames>https://api.qa.americanexpress.com, https://api.americanexpress.com,
     https://www206.americanexpress.com, https://fsgateway.aexp.com, 
     sftp://fsgateway.aexp.com, https://apigateway2s.americanexpress.com,
      https://api.qa2s.americanexpress.com, https://api.dev2s.americanexpress.com,
       https://apisl.americanexpress.com, https://sandbox.americanexpress.com, 
       https://www396.americanexpress.com, https://api-test.americanexpress.com,
       https://api2s.americanexpress.com, https://apigateway.americanexpress.com</hostnames>
    <state>retained</state>
    <created_at type="dateTime">2021-02-02T17:54:23Z</created_at>
    <updated_at type="dateTime">2021-02-02T17:54:23Z</updated_at>
    <credentials type="array">
      <credential>
        <name>app-id</name>
        <value type="integer">1234</value>
        <safe type="boolean">true</safe>
      </credential>
      <credential>
        <name>app-secret</name>
        <safe>false</safe>
      </credential>
    </credentials>
  </receiver>
  <payment_method>
    <token>QdjGCPSiYYDKxPMvvluYRG6zq79</token>
    <created_at type="dateTime">2021-02-02T19:54:55Z</created_at>
    <updated_at type="dateTime">2021-02-16T00:44:03Z</updated_at>
    <email>joey@example.com</email>
    <data nil="true"/>
    <storage_state>retained</storage_state>
    <test type="boolean">true</test>
    <metadata>
      <key>string value</key>
      <another_key type="integer">123</another_key>
      <final_key type="boolean">true</final_key>
    </metadata>
    <callback_url nil="true"/>
    <last_four_digits>0005</last_four_digits>
    <first_six_digits>378282</first_six_digits>
    <card_type>american_express</card_type>
    <first_name>Joe</first_name>
    <last_name>Jones</last_name>
    <month type="integer">3</month>
    <year type="integer">2032</year>
    <address1>33 Lane Road</address1>
    <address2>Apartment 4</address2>
    <city>Wanaque</city>
    <state>NJ</state>
    <zip>31331</zip>
    <country>US</country>
    <phone_number>919.331.3313</phone_number>
    <company>Acme Inc.</company>
    <full_name>Joe Jones</full_name>
    <eligible_for_card_updater type="boolean">true</eligible_for_card_updater>
    <shipping_address1>33 Lane Road</shipping_address1>
    <shipping_address2>Apartment 4</shipping_address2>
    <shipping_city>Wanaque</shipping_city>
    <shipping_state>NJ</shipping_state>
    <shipping_zip>31331</shipping_zip>
    <shipping_country>US</shipping_country>
    <shipping_phone_number>919.331.3313</shipping_phone_number>
    <payment_method_type>credit_card</payment_method_type>
    <errors>
    </errors>
    <verification_value></verification_value>
    <number>XXXX-XXXX-XXXX-0005</number>
    <fingerprint>3b71a994ea0b417babcab7111af5757d3ea8</fingerprint>
  </payment_method>
</transaction>
    """,
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
