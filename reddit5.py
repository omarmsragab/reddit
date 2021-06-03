import datetime
import requests
import praw
import json

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


# class for sybmission object
class SubmissionAnalyser:

    # "run" function that takes the url of the submission and runs "collect" and "summarize" functions 
    def run(self, url, limit):
        self.url = url
        self.limit = limit
        self.collect()
        self.summarize()

    # "collect" function that collects data before summarizing it
    def collect(self):
        # use the url of the submission to get data and convert it into a dictionary, then to an array of data
        response = requests.get(f'{self.url}.json', headers = {'User-agent': 'your bot 0.1'}).json()
        self.data = response[0]["data"]["children"][0]["data"]

        # setting up praw to use it later in the "summarize" function
        f = open('credentials.json')
        client_info = json.load(f)
        reddit = praw.Reddit(
            client_id = client_info["client_id"],
            client_secret = client_info["client_secret"],
            user_agent = "user_agent.0.1.0",
        )
        self.submission = reddit.submission(url = self.url)
        self.submission.comments.replace_more(limit=None)
        if type(self.limit) is int:
            self.comments = self.submission.comments.list()[:self.limit]
        else:
            self.comments = self.submission.comments.list()

    # "summarize" function that prints important data
    def summarize(self):
        
        # Printing the type and content of the submission

        # checking if the submission is a crosspost in order to get original tyoe and content from its parent
        parent_data = self.data
        if "crosspost_parent" in self.data:
            response = requests.get(f"http://reddit.com/comments/{self.data['crosspost_parent'].replace('t3_', '')}.json", headers = {'User-agent': 'your bot 0.1'}).json()
            parent_data = response[0]["data"]["children"][0]["data"]
        # printing type of content in the submission and printing the content
        if parent_data["selftext"] == '':
            if 'i.redd.it' in parent_data["url_overridden_by_dest"]:        # if submission is an image
                print("This submission is an image")
                print(f"Content: {parent_data['url_overridden_by_dest']}")
            elif 'v.redd.it' in parent_data["url_overridden_by_dest"]:      # if submission is a video directly posted to reddit
                print("This submission is a video")
                print(f"Content: {parent_data['secure_media']['reddit_video']['fallback_url']}")
            elif 'youtu' in parent_data["url_overridden_by_dest"]:          # if submission is a youtube video posted to reddit
                print("This submission is a video")
                print(f"Content: {parent_data['url_overridden_by_dest']}")
            else:                                                           # if submission is a link
                print("This submission is a link")
                print(f"Content: {parent_data['url_overridden_by_dest']}")                 
        else:                                                               # if submission is text
            print("This submission is a text")
            print("Content: " + parent_data["selftext"])


        # printing submission score and upvote ratio
        print(f"Score: {str(self.data['score'])}")
        print(f"Upvote ratio: {str(self.data['upvote_ratio'])}")


        # Printing the amount of comments for the submission
        if type(self.limit) is int:
            print(f"This submission has {str(self.data['num_comments'])} comments, but the user set the limit of comments to analyse to {self.limit}.")
        else:
            print(f"This submission has {str(self.data['num_comments'])} comments.")
        

        # Printing comment with most awards
        if len(self.comments) != 0:
            comments_bodies = []
            comments_awards = []
            # getting award count for all comments
            for comment in self.comments:
                comments_bodies.append(comment.body)
                response = requests.get(f'https://www.reddit.com/api/info.json?id=t1_{comment.id}&utm_source=reddit&utm_medium=usertext&utm_name=redditdev&utm_content=t1_{comment.id}', headers = {'User-agent': 'your bot 0.1'}).json()
                comments_awards.append(response["data"]["children"][0]["data"]["total_awards_received"])
            max_awards = max(comments_awards)
            # printing all comments that have the most awards if they all have that same number
            if max_awards != 0:
                for i,y in enumerate(comments_awards):
                    if y == max_awards:
                        print(f'The comment with the most awards is: "{comments_bodies[i]}"')


        # printing all comments that have the most upvotes if they all have that same number
        if len(self.comments) != 0:
            max_ups = max(comment.score for comment in self.comments)
            if max_ups != 0:
                for comment in self.comments:
                    if comment.score == max_ups:
                        print(f'The comment with the most upvotes is: "{comment.body}"')



# main function
def main():
    while True:
        # asking the user to choose job to do, either subreddit or submission/post, and then running the job
        job_type = input("Enter Job Type(Subreddit/Submission): ")
        if job_type.lower() == 'subreddit':
            sr_name = input("Enter subreddit Name: ")
            while True:
                limit = input("Enter number of submissions to analyse (leave blank for unlimited): ")
                if limit.isnumeric():
                    limit = int(limit)
                    break
                elif limit == '':
                    break
                else:
                    print("Value must be a number or blank, please try again.")
            subreddit = SubredditAnalyser()
            subreddit.run(sr_name, limit)
            break
        elif job_type.lower() == 'submission' or job_type.lower() == 'post':
            submission_url = input("Enter submission/post url: ")
            while True:
                limit = input("Enter number of comments to analyse (leave blank for unlimited): ")
                if limit.isnumeric():
                    limit = int(limit)
                    break
                elif limit == '':
                    break
                else:
                    print("Value must be a number or blank, please try again.")
            submission = SubmissionAnalyser()
            submission.run(submission_url, limit)
            break
        else:
            print("Job type not defined, please try again.") # reasking the user to choose the job if choice  isn't clear
if __name__ == '__main__':    
    main()