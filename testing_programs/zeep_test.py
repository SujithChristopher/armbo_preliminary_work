from zeep import Client


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

args = {
        "conferencecode": conferenct,
        "conferenceyear": conferenceyear,
        "bankname": paymode,
        "remoteip": remoteip,
        "regno": apno,
        "candidatename": name,
        "nameinreceipt": name,
        "address1": address,
        "address2": adress1,
        "city": city,
        "state": state,
        "country": country,
        "pincode": pincode,
        "phone": phone,
        "mobile": mob,
        "email": email,
        "foodtype": foodtype,
        "participanttype": participanttype,
        "practicetype": practicetype,
        "accompanymembers": members,
        "paymentamount": "100",
        "ToWards": tods,
        "Allow80G": all80,
        "PanCardNo": pan,
        "hasgst": hast,
        "GSTReg": gst,
        "gstnumber": gst1,
        "gstmobileno": gst2,
        "gstemailid": gst3,
        "inputcaption1": inp1,
        "inputvalue1": inp2,
        "inputcaption2": inp3,
        "inputvalue2": inp4,
        "inputcaption3": inp5,
        "inputvalue3": inp6,
        "inputcaption4": inp7,
        "inputvalue4": inp8,
        "inputcaption5": inp9,
        "inputvalue5": inp10
    }


client = Client("https://clin.cmcvellore.ac.in/TestConference/conferencepay.asmx?wsdl")


response = client.service.NEWCONFONLINEPAYSAVE(args=args)
