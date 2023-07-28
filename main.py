import requests
import time
import smtplib


def test_api(jwt):
    response = requests.get("you_api_here", headers={"Authorization": "Bearer {}".format(jwt)})
    if response.status_code != 200:
        raise Exception(f"{response.status_code}")


def send_email(subject, body):
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login("sender_email_here", "password_here")
    message = "Subject: {}\n\n{}".format(subject, body)
    server.sendmail("sender_email_here", "destination_email_here", message)


def main():
    jwt = "your_jwt_here"
    now = time.time()
    next_test = now + 900  # 15 minutes

    while True:
        if time.time() >= next_test:
            try:
                test_api(jwt)
            except Exception as err:
                subject = "API health notification"
                body = "The API is not right. Error message: {}".format(str(err))
                send_email(subject, body)

            next_test = time.time() + 900  # 15 minutes

        time.sleep(60)  # 1 minute


if __name__ == "__main__":
    main()
