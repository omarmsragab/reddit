import requests
import praw
import json

# class for sybmission object
class SubmissionAnalyser:

    # "run" function that takes the url of the submission and runs "collect" and "summarize" functions 
    def run(self, url, limit, depth):
        self.url = url
        self.limit = limit
        self.depth = depth
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
        self.comments = []

        # recursive function that appends all comments within the depth set by the user to the "self.comments" list
        def Comment_tree(current_level_comment_list, depth):
            next_level_comments_list = []
            for current_level_comment in current_level_comment_list:
                self.comments.append(current_level_comment)
                next_level_comments_list.extend(current_level_comment.replies)
            if depth > 1:
                Comment_tree(next_level_comments_list, depth - 1)

        # adding all comments to the "self.comments" list if user set depth to 0, otherwise call the recusrive function "comment_tree"
        if self.depth == 0:
            self.comments = self.submission.comments.list()
        else:
            Comment_tree(self.submission.comments, self.depth)

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