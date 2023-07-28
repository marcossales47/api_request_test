import requests
import time
import smtplib


def test_api(jwt):
    response = requests.get("https://api.tisaude.com/api/login", headers={"Authorization": "Bearer {}".format(jwt)})
    if response.status_code != 200:
        raise Exception(f"{response.status_code}")


def send_email(subject, body):
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login("marcos-ius@live.com", "D5F@MnQd")
    message = "Subject: {}\n\n{}".format(subject, body)
    server.sendmail("marcos-ius@live.com", "marcos.sales@tisaude.com", message)


def main():
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLnRpc2F1ZGUuY29tIiwiaWF0IjoxNjkwMzkyMzYxLCJleHAiOjE2OTI5ODQzNjEsIm5iZiI6MTY5MDM5MjM2MSwianRpIjoiN081YlFjMVFFeVNCTmJQMyIsInN1YiI6MTUwMDAsInBydiI6IjU4NzA4NjNkNGE2MmQ3OTE0NDNmYWY5MzZmYzM2ODAzMWQxMTBjNGYifQ.cLxLN72LZh8d0nm7_waWz7C59a0M8cPfVTtAAaJ1uu8"
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
