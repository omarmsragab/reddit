from serializers.subreddit import *
from serializers.post import *

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

    # "collect" function that collects various information about the subreddit
    def collect(self):
        serialized_subreddit = Subreddit(self.subreddit)
        serialized_posts = []
        for submission in self.sorted_subreddit:
            serialized_post = Post(submission)
            serialized_posts.append(serialized_post)
            # if submission.score > self.most_upvotes:
            #     self.most_upvotes = submission.score
            #     self.most_upvotes_submission = submission.title
            # if submission.num_comments > self.most_comments:
            #     self.most_comments = submission.num_comments
            #     self.most_comments_submission = submission.title
            # if datetime.datetime.fromtimestamp(submission.created_utc) < self.oldest_utc:
            #     self.oldest_utc = datetime.datetime.fromtimestamp(submission.created_utc)
            #     self.oldest_submission = submission.title
            # if datetime.datetime.fromtimestamp(submission.created_utc) > self.most_recent_utc:
            #     self.most_recent_utc = datetime.datetime.fromtimestamp(submission.created_utc)
            #     self.most_recent_submission = submission.title
        
        