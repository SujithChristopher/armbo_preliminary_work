import requests
# SOAP request URL
  
# structured XML


paymode = "PAYU"
userName = "CNOAPMI"
password = "dYRsJ7rt"
apno = "AMPICON"
name = ""
mob = ""
conferenct = "AMPICON"
conferenceyear = "2022"
title3 = ""
fud1 = ""
address = "" + "$w('#input7').value;"
adress1 = "" + "$w('#input8').value;"
city = "" + "$w('#input10').value;"
state = "" + "$w('#input9').value;"
pincode = "" + "$w('#input11').value;"
phone = "" + "$w('#input4').value;"
mobile = ""
email = "" + "$w('#input3').value;"
foodtype = ""
participanttype = ""
practicetype = ""
members = ""
remoteip = ""
tods = "-"
all80 = "No"
hast = ""
member = ""
country = ""
gst = ""
pan = ""
gst2 = ""
gst3 = ""
gst1 = ""
inp1 = ""
inp2 = ""
inp3 = ""
inp4 = ""
inp5 = ""
inp6 = ""
inp7 = ""
inp8 = ""
inp9 = ""
inp10 = ""
payload = f"""
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <UserDetails xmlns="http://www.cmch-vellore.edu/">
      <userName>{userName}</userName>
      <password>{password}</password>
      <program>{apno}</program>
    </UserDetails>
  </soap:Header>
  <soap:Body>
    <NEWCONFONLINEPAYSAVE xmlns="http://www.cmch-vellore.edu/">
      <conferencecode>string</conferencecode>
      <conferenceyear>string</conferenceyear>
      <bankname>string</bankname>
      <remoteip>string</remoteip>
      <regno>string</regno>
      <candidatename>string</candidatename>
      <nameinreceipt>string</nameinreceipt>
      <address1>string</address1>
      <address2>string</address2>
      <city>string</city>
      <state>string</state>
      <country>string</country>
      <pincode>string</pincode>
      <phone>string</phone>
      <mobile>string</mobile>
      <email>string</email>
      <foodtype>string</foodtype>
      <participanttype>string</participanttype>
      <practicetype>string</practicetype>
      <accompanymembers>string</accompanymembers>
      <paymentamount>100</paymentamount>
      <ToWards>string</ToWards>
      <Allow80G>string</Allow80G>
      <PanCardNo>string</PanCardNo>
      <hasgst>string</hasgst>
      <GSTReg>string</GSTReg>
      <gstnumber>string</gstnumber>
      <gstmobileno>string</gstmobileno>
      <gstemailid>string</gstemailid>
      <inputcaption1>string</inputcaption1>
      <inputvalue1>string</inputvalue1>
      <inputcaption2>string</inputcaption2>
      <inputvalue2>string</inputvalue2>
      <inputcaption3>string</inputcaption3>
      <inputvalue3>string</inputvalue3>
      <inputcaption4>string</inputcaption4>
      <inputvalue4>string</inputvalue4>
      <inputcaption5>string</inputcaption5>
      <inputvalue5>string</inputvalue5>
    </NEWCONFONLINEPAYSAVE>
  </soap:Body>
</soap:Envelope>"""

url = "https://clin.cmcvellore.ac.in/testconference/ConferencePay.asmx"


headers = {
    "UserDetails":{"userName":userName,"password":password,"program":apno},
}
# POST request
response = requests.request("POST", url, headers=headers, data=payload)
# prints the response
print(response.text)
print(response)