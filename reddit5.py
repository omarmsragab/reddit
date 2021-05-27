import datetime
import time
import requests
import praw

# class for subreddit object
class SubReddit:   

    # "run" function that takes the name of the subreddit and runs "collect" and "summarize" functions 
    def run(self, name):
        self.name = name
        self.collect()
        self.summarize()

    # "collect" function that takes the url of the subreddit and converts it to a dictionary, then to an array of posts
    def collect(self):
        self.posts = []
        last_post_id = "null"
        while True:
            r = requests.get('https://www.reddit.com/r/' + self.name + '.json?after=' + last_post_id, headers = {'User-agent': 'your bot 0.1'}).json()
            time.sleep(2.1)
            x = r["data"]
            self.posts.extend(x["children"]) # put posts in an array of dictionaries
            last_post_id = x["after"]
            if last_post_id == None:
                break
            

    # "summarize" function that prints important data
    def summarize(self):

        # print the number of posts in the subreddit
        print(f"This subreddit contains {len(self.posts)} posts.")
        
        
        # print the name of the post with the most upvote and how many upvotes it has
        
        # putting numbers of most upvotes in an array
        ups = []
        for  i in range(len(self.posts)):
            post = self.posts[i]
            post_data = post["data"]
            ups.append(post_data["ups"])
        max_ups = max(ups)
        # printing all posts that have the max number of upvotes if they all have that same number
        if max_ups != 0:
            for i,y in enumerate(ups):
                if y == max_ups:
                    max_location = i
                    max_ups_post = self.posts[max_location]
                    post_data = max_ups_post["data"]
                    print(f"The name of the post with most upvotes is \"{post_data['title']}\" with {max_ups} upvotes.")
        

        # print the name of the post with the most upvote and how many upvotes it has

        # Putting number of comments on each post in an array
        comments_count = []
        for  i in range(len(self.posts)):
            post = self.posts[i]
            post_data = post["data"]
            comments_count.append(post_data["num_comments"])
        max_comments = max(comments_count)
        # printing all posts that have the max number of comments if they all have that same number
        if max_comments != 0:
            for i,y in enumerate(comments_count):
                if y == max_comments:
                    max_location = i
                    max_comments_post = self.posts[max_location]
                    post_data = max_comments_post["data"]
                    print(f"The name of the post with most comments is \"{post_data['title']}\" with {max_comments} comments.")
        

        # print the name of the oldest post and the date it was posted

        # Putting creation times of each post in an array
        creation_utc = []
        for  i in range(len(self.posts)):
            post = self.posts[i]
            post_data = post["data"]
            creation_utc.append(post_data["created_utc"])
        min_creation_utc = min(creation_utc)
        creation_time = datetime.datetime.fromtimestamp(min_creation_utc) # changing the times from the utc format to the date/time format
        # printing all posts that have the oldest creation date if they all have that same number
        for i,y in enumerate(creation_utc):
            if y == min_creation_utc:
                min_location = i
                min_creation_utc_post = self.posts[min_location]
                post_data = min_creation_utc_post["data"]
                print(f"The name of the oldest post is \"{post_data['title']}\" and it was created on {creation_time}.")
        

        # print the name of the most recent post and the date it was posted

        # Putting creation times of each post in an array
        max_creation_utc = max(creation_utc)
        creation_time = datetime.datetime.fromtimestamp(max_creation_utc) # changing the times from the utc format to the date/time format
        # printing all posts that have the newest creation date if they all have that same number
        for i,y in enumerate(creation_utc):
            if y == max_creation_utc:
                max_location = i
                max_creation_utc_post = self.posts[max_location]
                post_data = max_creation_utc_post["data"]
                print(f"The name of the most recent post is \"{post_data['title']}\" and it was created on {creation_time}.")


# class for sybmission object
class Submission:

    # "run" function that takes the url of the submission and runs "collect" and "summarize" functions 
    def run(self, url):
        self.url = url
        self.collect()
        self.summarize()

    # "collect" function that collects data before summarizing it
    def collect(self):
        # use the url of the submission to get data and convert it into a dictionary, then to an array of data
        r = requests.get(self.url + '.json', headers = {'User-agent': 'your bot 0.1'}).json()
        a = r[0]
        b = a["data"]
        c = b["children"]
        d = c[0]
        self.data = d['data']

        # setting up praw to use it later in the "summarize" function
        reddit = praw.Reddit(
            client_id="LeXZgJzUgQ5Hag",
            client_secret="x6OoIUMtJuUgmFTV2ym0j07-HnuF5g",
            user_agent="user_agent.0.1.0",
        )
        self.submission = reddit.submission(url = self.url)
        self.submission.comments.replace_more(limit=None)

    # "summarize" function that prints important data
    def summarize(self):
        
        # Printing the type and content of the submission

        # checking if the submission is a crosspost in order to get original tyoe and content from its parent
        parent_data = self.data
        if "crosspost_parent" in self.data:
            r = requests.get('http://reddit.com/comments/' + self.data["crosspost_parent"].replace('t3_', '') + '.json', headers = {'User-agent': 'your bot 0.1'}).json()
            a = r[0]
            b = a["data"]
            c = b["children"]
            d = c[0]
            parent_data = d['data']
        # printing type of content in the submission and printing the content
        if parent_data["selftext"] == '':
            if 'i.redd.it' in parent_data["url_overridden_by_dest"]:        # if submission is an image
                print("This submission is an image")
                print("Content: " + parent_data["url_overridden_by_dest"])
            elif 'v.redd.it' in parent_data["url_overridden_by_dest"]:      # if submission is a video directly posted to reddit
                print("This submission is a video")
                r = parent_data["secure_media"]
                a = r["reddit_video"]
                print("Content: " + a["fallback_url"])
            elif 'youtu' in parent_data["url_overridden_by_dest"]:          # if submission is a youtube video posted to reddit
                print("This submission is a video")
                print("Content: " + parent_data["url_overridden_by_dest"])
            else:                                                           # if submission is a link
                print("This submission is a link")
                print("Content: " + parent_data["url_overridden_by_dest"])                 
        else:                                                               # if submission is text
            print("This submission is a text")
            print("Content: " + parent_data["selftext"])


        # printing submission score and upvote ratio
        print("Score: " + str(self.data["score"]))
        print("Upvote ratio : " + str(self.data["upvote_ratio"]))


        # Printing the amount of comments for the submission
        print("This submission has " + str(self.data["num_comments"]) + " comments.")
        

        # Printing comment with most awards
        if len(self.submission.comments.list()) != 0:
            comments_bodies = []
            comments_awards = []
            # getting award count for all comments
            for comment in self.submission.comments.list():
                comments_bodies.append(comment.body)
                r = requests.get('https://www.reddit.com/api/info.json?id=t1_' + comment.id + '&utm_source=reddit&utm_medium=usertext&utm_name=redditdev&utm_content=t1_' + comment.id, headers = {'User-agent': 'your bot 0.1'}).json()
                a = r["data"]
                b = a["children"]
                c = b[0]
                comment_data = c["data"]
                comments_awards.append(comment_data["total_awards_received"])
            max_awards = max(comments_awards)
            # printing all comments that have the most awards if they all have that same number
            if max_awards != 0:
                for i,y in enumerate(comments_awards):
                    if y == max_awards:
                        print('The comment with the most awards is: "' + comments_bodies[i] + '"')


        # printing comment with most upvotes
        if len(self.submission.comments.list()) != 0:
            comments_ups = []
            for comment in self.submission.comments.list():
                comments_ups.append(comment.score)
            max_ups = max(comments_ups)
            # printing all comments that have the most upvotes if they all have that same number
            if max_ups != 0:
                for i,y in enumerate(comments_ups):
                    if y == max_ups:
                        print('The comment with the most upvotes is: "' + comments_bodies[i] + '"')



# main function
def main():
    while True:
        # asking the user to choose job to do, either subreddit or submission/post, and then running the job
        job_type = input("Enter Job Type(Subreddit/Submission): ")
        if job_type == 'Subreddit' or job_type == 'subreddit':
            sr_name = input("Enter SubReddit Name: ")
            subreddit = SubReddit()
            subreddit.run(sr_name)
            break
        elif job_type == 'Submission' or job_type == 'submission' or job_type == 'Post' or job_type == 'post':
            submission_url = input("Enter submission/post url: ")
            submission = Submission()
            submission.run(submission_url)
            break
        else:
            print("Job type not defined, please try again.") # reasking the user to choose the job if choice  isnn't clear
if __name__ == '__main__':    
    main()