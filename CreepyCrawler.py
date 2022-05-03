import requests
import os
import json
import string

bearer_token = 'AAAAAAAAAAAAAAAAAAAAALzgWQEAAAAA%2FC9JJC0bpa53VtdJtK6t7WyCWdg%3Dwg0pdQWcvOLLCHW0EJw1Nb5X97tI9neonqOTrD4L6NFEHIwSJo'

def create_url_pullTweets(id):
    user_id = id
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def create_url_userInfo(user):
    usernames = f"usernames={user}"
    user_fields = "user.fields=id"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def get_params():
    return {"tweet.fields": "created_at"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

def connect_to_endpoint_pullTweet(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def connect_to_endpoint_userInfo(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def create_dictionary(tweets):
    dictionary = []
    for tweet in tweets:
            for word in tweet.split(" "):
                raw_word = word.translate(str.maketrans('', '', string.punctuation))
                if "\xa0" in raw_word:
                    raw_words = raw_word.split("\xa0")
                    for i in raw_words:
                        dictionary.append(i)
                else:
                    if raw_word[:8] != "httpstco":
                        dictionary.append(raw_word)

    return set(dictionary)


def write_to_file(dictionary, user):
    filename = f"{user}_dictionary.txt"
    with open(filename, 'w') as f:
        for word in dictionary:
            try:
                f.write(word)
                f.write('\n')
            except:
                pass
            

def pull_user_id(user):
    url = create_url_userInfo(user)
    json_response = connect_to_endpoint_userInfo(url)
    return json_response["data"][0]["id"]


def print_menu(user, incRT):
    print(f"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
Welcome to CreepyCrawler - The social media dictionary generator!

Please select an option from the menu below:
1. Set username to scan - Current: {"Not Set" if user == "" else user}
2. Include retweets in scan - Current: {"False" if not incRT else "True"}
3. Run scan and compile dictionary
4. Exit
    """)
    choice = int(input("Choice: "))
    if choice == 1:
        return input("Username: "), incRT, False
    elif choice == 2:
        if input("T/F: ").upper() == "T":
            return user, True, False
        else:
            return user, False, False
    elif choice == 3:
        return user, incRT, True
    elif choice == 4:
        exit()
    else:
        print("Not a valid option")

    


def main():
    user = ""
    incRT = False
    while True:
        
        run = False
        tweets = []
        

        while run == False:
            user, incRT, run = print_menu(user, incRT)

        user_ID = pull_user_id(user)


        url_pullTweets = create_url_pullTweets(user_ID)
        params_pullTweets = get_params()
        json_response_pullTweets = connect_to_endpoint_pullTweet(url_pullTweets, params_pullTweets)
        for i in range(0,10):
            text = json_response_pullTweets["data"][i]['text'].replace('\n',' ')
            if incRT:
                tweets.append(text)
            else:
                if text[:2] != "RT": # Filter out retweets by looking for 'RT' at the beginning of the text field
                    tweets.append(text)
        
        dictionary = create_dictionary(tweets)
        write_to_file(dictionary, user)


if __name__ == "__main__":
    main()