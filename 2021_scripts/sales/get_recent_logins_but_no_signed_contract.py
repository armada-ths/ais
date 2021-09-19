import datetime

from companies.models import SignupLog

signup_logs = SignupLog.objects.filter()

for signup_log in signup_logs:
  start_date = datetime.datetime(2021, 6, 4, 0, 0)
  end_date = datetime.datetime(2021, 6, 22, 23, 59)
  timestamp = signup_log.timestamp
  if start_date < timestamp and timestamp < end_date:
    print()
    print(f"--- {signup_log.company} ---")
    print(signup_log.company_contact)
    print(timestamp)
    print("---")


out = 'Name\tRole'


# for application in applications:
# 	out += '\n'
# 	out += application.user.first_name + " " + application.user.last_name
# 	out += '\t'
# 	out += application.delegated_role.name
# print(out)

# fh = open('contact_info.txt', 'w')
# fh.write(out)
# fh.close()