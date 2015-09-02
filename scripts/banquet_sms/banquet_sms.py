# -*- coding: utf-8 -*-
'''
# *WARNING* Be sure that the encoding of this file is UTF-8.
# Lots of terminals run in latin-1 for example,
# so if you edit with vim and save, it will be latin-1 again.
'''
import sys
import csv
import urllib

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
        # Read the CSV as a python dict
        banquet_attendence = csv.DictReader(csvfile, delimiter=';')
        for attendee in banquet_attendence:
            # This simply strips out everything that is not a number (1234567890)
            phone_number="".join(_ for _ in attendee['Cell Phone Number'] if _ in "1234567890")

            if phone_number.startswith("07"):
                phone_number=phone_number[1:]

            if phone_number.startswith("46"):
                phone_number=phone_number[2:]

            phone_number="46"+phone_number
            send_to_this=1
            if len(phone_number)!=11:
                error_file.write("Phone number error: "+phone_number+"("+attendee['Cell Phone Number']+"), ")
                send_to_this=0

            if attendee['Table']=="" or attendee['Placement Number']=="":
                error_file.write("Placement error, ")
                send_to_this=0

            if send_to_this:
                #touple will be (phone_number, message)
                attendees.append( (phone_number, make_message_for(attendee)) )
                number_of_readins += 1
            else:
                error_file.write("Error with "+attendee['Name']+"(id:"+attendee['Id']+")\n")
                number_of_errors += 1

    print("\nWe had %d errors, but %d attendee's where read in correctly, see errors.txt for more information.\n"%(number_of_errors, number_of_readins))
    print("A total of %d text messages will be sent out. The price will be %.2f SEK" % (len(attendees), len(attendees)*0.50 ))
    print("Would you like to continue? (yes/no)") 
    error_file.close()
    choice = raw_input().lower()
    
    if choice=="yes":
        for attendee in attendees:
            try:
                number=attendee[0]
                message=attendee[1]
                print("To: %s\n%s\n" % (number, message) )
                send_sms(number, message)
            except Exception as inst:
                print(type(inst))
                print(inst)
    else:
        print("Operation canceled.\nNo texts have been sent, you may fix any errors and then try again.")

main()
