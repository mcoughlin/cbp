import cbp_notifications

def main():
    test_email = cbp_notifications.cbp_email.CbpEmail(msg="This is a test email for the email notification inside cbp class",sender="eric.coughlin2014@gmail.com",recipients="eric.coughlin2014@gmail.com",subject="[CBP Notification] Test")
    test_email.send()
    print("done")

main()
