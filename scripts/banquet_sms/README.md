# Banquet SMS Service
This is the Banquet SMS service used with the legacy Niwen system.

How to use:
1. After placement is done, export all the Attendence data from niwen 
   with the Banquet/Export to excel button.

2. Run the script with the csv file as a arguement, example:
   "python banquet_sms.py gasque_attendance-20150826144303.csv"
   (Given that the csv file is in the same folder as the script)

3. The script will process the CSV file and generate and error.txt file.
   The error files contains the people that sms would not be sent to.
   This can be because placement was missing (Maybe only a table and no
   seat?) or because the phone number is not valid.

4. If you are not happy with the errors, answer no, and no SMS's will 
   be sent. You can then correct the errors in Niwen, and go back to 
   step #1.

5. If you are happy with the errors, answer 'yes' and the script will 
   send out the SMS's. This might take a while, since it does this 
   one number at a time, and has to make a HTTP connection for each.
    
