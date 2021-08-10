import datetime

# class for subreddit object
class SubredditAnalyzer:   

    # "run" function that sets up the subreddit and runs "collect" and "summarize" functions 
    def run(self, reddit, name, post_limit, sort_by, sort_by_top_range):
        self.subreddit = reddit.subreddit(name)
        if sort_by == 'new':
            self.sorted_subreddit = self.subreddit.new(limit=post_limit)
        elif sort_by == 'rising':
            self.sorted_subreddit = self.subreddit.rising(limit=post_limit)
        elif sort_by == 'controversial':
            self.sorted_subreddit = self.subreddit.controversial(limit=post_limit)
        elif sort_by == 'top':
            self.sorted_subreddit = self.subreddit.top(sort_by_top_range, limit=post_limit)
        elif sort_by == 'gilded':
            self.sorted_subreddit = self.subreddit.gilded(limit=post_limit)
        self.collect()
        self.summarize()

    # "collect" function that collects various information about the subreddit
    def collect(self):
        self.id = self.subreddit.id
        self.name = self.subreddit.display_name
        self.full_name = self.subreddit.name
        self.description = self.subreddit.description
        self.public_description = self.subreddit.public_description
        self.subscriber_count = self.subreddit.subscribers
        self.submission_count = 0
        for submission in self.subreddit.hot(limit=None):
            self.submission_count += 1
        self.created_time = datetime.datetime.fromtimestamp(self.subreddit.created_utc)
        self.is_NSFW = self.subreddit.over18
        self.rules = []
        for rule in self.subreddit.rules:
            self.rules.append(rule)
        self.submissions = []
        self.most_upvotes_submission = ''
        self.most_upvotes = 0
        self.most_comments_submission = ''
        self.most_comments = 0
        self.oldest_submission = ''
        self.oldest_utc = datetime.datetime.utcnow()
        self.most_recent_submission = ''
        self.most_recent_utc = datetime.datetime.fromtimestamp(0)
        for submission in self.sorted_subreddit:
            self.submissions.append(submission)
            if submission.score > self.most_upvotes:
                self.most_upvotes = submission.score
                self.most_upvotes_submission = submission.title
            if submission.num_comments > self.most_comments:
                self.most_comments = submission.num_comments
                self.most_comments_submission = submission.title
            if datetime.datetime.fromtimestamp(submission.created_utc) < self.oldest_utc:
                self.oldest_utc = datetime.datetime.fromtimestamp(submission.created_utc)
                self.oldest_submission = submission.title
            if datetime.datetime.fromtimestamp(submission.created_utc) > self.most_recent_utc:
                self.most_recent_utc = datetime.datetime.fromtimestamp(submission.created_utc)
                self.most_recent_submission = submission.title
 
    # "summarize" function that prints collected data
    def summarize(self):

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Full Name: {self.full_name}")
        print(f"Description: {self.description}")
        print(f"Public Description: {self.public_description}")
        print(f"Number of Subscribers: {self.subscriber_count}")
        print(f"Number of Submissions: {self.submission_count}")
        print(f"Created Time: {self.created_time}")
        print(f"Is NSFW: {self.is_NSFW}")
        print(f"Rules: {self.rules}")
        print(f"Submissions Collected For Analyse ({len(self.submissions)}): {self.submissions}")
        print(f"The title of the post with most upvotes is '{self.most_upvotes_submission}' with {self.most_upvotes} upvotes.")
        print(f"The title of the post with most comments is '{self.most_comments_submission}' with {self.most_comments} comments.")
        print(f"The title of the oldest post is '{self.oldest_submission}' and it was created on {self.oldest_utc}.")
        print(f"The title of the most recent post is '{self.most_recent_submission}' and it was created on {self.most_recent_utc}.")