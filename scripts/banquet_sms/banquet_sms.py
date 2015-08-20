# -*- coding: utf-8 -*-
import sys
import csv
import re
import urllib
'''
def send_sms(phone_number, message):
    sms_url='http://smsserver.pixie.se/sendsms?'
    data=urllib.urlencode({
                            'account':'10910843',
                            'pwd':'wecuTE2U',
                            'receivers':phone_number,
                            'sender':'Armada',
                            'message':message
                            })
    sms_service = urllib.urlopen(sms_url+data)
    response = sms_service.read()
    sms_service.close()
    return response
'''
def make_message_for(attendee):
    name=attendee['Name'].split(" ")
    name=name[0]
    message="Välkommen till banquet "+name+", du sitter vid bord "+attendee['Table']+" vid plats "+attendee['Placement Number']+"."
    return message

def main():
    attendees=[]
    error_file = open('errors.txt', 'w')
    number_of_errors = 0
    number_of_readins = 0

    with open(str(sys.argv[1]), 'rb') as csvfile:
        banquet_attendence = csv.DictReader(csvfile, delimiter=';')
        for attendee in banquet_attendence:
            phone="".join(_ for _ in attendee['Cell Phone Number'] if _ in "1234567890")
            if phone.startswith("07"):
                phone=phone[1:]

            if phone.startswith("46"):
                phone=phone[2:]

            phone="46"+phone
            send_to_this=1
            if len(phone)!=11:
                error_file.write("Phone number error: "+phone+"("+attendee['Cell Phone Number']+"), ")
                send_to_this=0

            if attendee['Table']=="" or attendee['Placement Number']=="":
                error_file.write("Placement error, ")
                send_to_this=0

            if send_to_this:
                #touple will be (phone_number, message)
                attendees.append( (phone, make_message_for(attendee)) )
                number_of_readins += 1
            else:
                error_file.write("Error with "+attendee['Name']+"(id:"+attendee['Id']+")\n")
                number_of_errors += 1

    print("\nWe had %d errors, but %d attendee's where read in correctly, see errors.txt for more information.\n"%(number_of_errors, number_of_readins))
    print("A total of %d text messages will be sent out. The price will be %.2f SEK" % (len(attendees), len(attendees)*0.50 ))
    print("Would you like to continue? (yes/no)")
    choice = raw_input().lower()
    if choice=="yes":
        for attendee in attendees:
            try:
                number=attendee[0]
                message=attendee[1]
                print("To: %s\n%s\n" % (number, message) )

            except Exception as inst:
                print(type(inst))
                print(inst)
                error_file.write("ERROR TYPE: %s\nERROR INSTANCE: %s"%(type(inst),inst))
    else:
        print("Operation canceled.\nNo texts have been sent, you may fix any errors and then try again.")
    error_file.close()

    #input("Press Enter to continue...")

#send_sms(number, message)
            #'46707925506'
            #'så mörkt är det nu\nmen snön är inte på åkern än!'
main()
#send_sms('46707925506', 'så mörkt är det nu\nmen snön är inte på åkern än!')
#Response: <?xml version="1.0" encoding = "ISO-8859-1" ?><response code="0"><cost>50</cost></response>
