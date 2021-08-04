import datetime
import requests

# class for subreddit object
class SubredditAnalyser:   

    # "run" function that takes the name of the subreddit and runs "collect" and "summarize" functions 
    def run(self, name, limit):
        self.name = name
        self.limit = limit
        self.collect()
        self.summarize()

    # "collect" function that takes the url of the subreddit and converts it to a dictionary, then to an array of posts
    def collect(self):
        self.posts = []
        self.post_count = 0
        limit_not_reached = True
        last_post_id = "null"
        while True:
            response = requests.get(f'https://www.reddit.com/r/{self.name}.json?after={last_post_id}', headers = {'User-agent': 'your bot 0.1'}).json()
            last_post_id = response["data"]["after"]
            self.post_count += response["data"]["dist"]
            if limit_not_reached:
                self.posts.extend(response["data"]["children"]) # put posts in an array of dictionaries
                if type(self.limit) is int:
                    if len(self.posts) == self.limit:
                        limit_not_reached = False
                    elif len(self.posts) > self.limit:
                        extra = len(self.posts) - self.limit
                        del self.posts[-extra:]
                        limit_not_reached = False
            if last_post_id == None:
                break
            
    # "summarize" function that prints important data
    def summarize(self):

        # print the number of posts in the subreddit
        if type(self.limit) is int:
            print(f"This subreddit contains {self.post_count} posts, but the user set the limit of submissions to analyse to {self.limit}.")
        else:
            print(f"This subreddit contains {self.post_count} posts.")
        
        
        # print the name of the post with the most upvote and how many upvotes it has
        
        max_ups = max(post["data"]["ups"] for post in self.posts)
        # printing all posts that have the max number of upvotes if they all have that same number
        if max_ups != 0:
            for post in self.posts:
                if post["data"]["ups"] == max_ups:
                    print(f"The name of the post with most upvotes is \"{post['data']['title']}\" with {max_ups} upvotes.")
        

        # print the name of the post with the most upvote and how many upvotes it has

        max_comments = max(post["data"]["num_comments"] for post in self.posts)
        # printing all posts that have the max number of comments if they all have that same number
        if max_comments != 0:
            for post in self.posts:
                if post["data"]["num_comments"] == max_comments:
                    print(f"The name of the post with most comments is \"{post['data']['title']}\" with {max_comments} comments.")
        

        # print the name of the oldest post and the date it was posted

        min_creation_utc = min(post["data"]["created_utc"] for post in self.posts)
        # printing all posts that have the oldest creation date if they all have that same number
        for post in self.posts:
            if post["data"]["created_utc"] == min_creation_utc:
                print(f"The name of the oldest post is \"{post['data']['title']}\" and it was created on {datetime.datetime.fromtimestamp(min_creation_utc)}.")
        

        # print the name of the most recent post and the date it was posted

        max_creation_utc = max(post["data"]["created_utc"] for post in self.posts)
        # printing all posts that have the newest creation date if they all have that same number
        for post in self.posts:
            if post["data"]["created_utc"] == max_creation_utc:
                print(f"The name of the most recent post is \"{post['data']['title']}\" and it was created on {datetime.datetime.fromtimestamp(max_creation_utc)}.")