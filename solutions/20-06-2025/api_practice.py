import requests
import json


URL = "https://jsonplaceholder.typicode.com/users"
URL_2 = "https://dummyjson.com/users"


# 1) first request to return users' names


def solution_1(link: str) -> str:
    response = requests.get(link)
    return "\n".join([user["name"] for user in response.json()])


# 2) return names and emails of users who are living in "South Christy"

def solution_2(link: str) -> str:
    params = {"city": "South Christy"}
    response = requests.get(link, params=params)
    return "\n".join([f"Name: {user["name"]}\tEmail: {user["email"]}" for user in response.json()])


# 3) find all users who have "Group" word in there company name
# and save their names and company names in file group_users.json

def solution_3(link: str, json_file_name: str) -> str:
    response = requests.get(link)
    group_users = [{"User's name": user["name"],"Company name": user["company"]["name"]} for user in response.json()
              if "Group" in user["company"]["name"]]
    with open(json_file_name, "w", encoding="utf-8", newline="") as f:
        json.dump(group_users, f, indent=2)
    return f"{len(group_users)} users saved to group_users.json"


class Practice:

    def __init__(self, link: str) -> None:
        try:
            self.response = requests.get(link)
        except Exception as e:
            print(f"Error raised: {type(e).__name__} - {e}")
        # keep all information about users
        self.users_data = self.response.json()['users']

        # keep the track about user's info
        self.users: list[dict[str, str]] = [
            {'name': user['firstName'] + user['lastName']} for user in self.users_data
        ]

    # 4) request to URL_2, take list of names and mails,
    # return amount of users

    def amount_of_users(self) -> int:
        return len(self.users)

    # 5) Take only that who is older than 30

    def older_than_30(self) -> list[dict[str, str | int]] | str:
        if self.response.status_code in [500, 404]:
            return f"Bad output from server: {self.response.status_code}, error raised"
        older_than_30 = [{'name': user_data['firstName'] + user_data['lastName'], 'age': user_data['age'],
                          'email': user_data['email']} for user_data in self.users_data if user_data['age'] > 30]
        return older_than_30

    def summary(self) -> dict[str, list[any]]:
        summary = {"total": self.amount_of_users(),
                   "older_than_30": self.older_than_30()
                   }
        return summary

    def post_request(self, link, data: dict[str, str]) -> str:
        response = requests.post(link, json=data)
        token = response.json().get("token")
        print("TOKEN:", token)
        #print(f"token: {token}, type: {type(token)}")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        new_response = requests.get("https://dummyjson.com/auth/me", headers=headers)
        print("Auth response:", new_response.text)


link_1 = "https://dummyjson.com/auth/login"
data = {
  "username": "kminchelle",
  "password": "0lelplR"
}

y = Practice(URL_2)
y.post_request(link_1, data)


