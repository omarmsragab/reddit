from serializers.subreddit import *
from serializers.post import *


class KeywordAnalyzer:

    def run(self, reddit, keyword, subreddit_limit, post_limit):
        self.all_subreddits = reddit.subreddits
        self.all_submissions = reddit.subreddit("all")
        self.keyword = keyword
        self.subreddit_limit = subreddit_limit
        self.post_limit = post_limit
        self.collect()
    
    def collect(self):
        serialized_subreddits = []
        for subreddit in self.all_subreddits.search(self.keyword, limit=self.subreddit_limit):
            serialized_subreddit = Subreddit(subreddit)
            serialized_subreddits.append(serialized_subreddit)

        serialized_posts = []
        for submission in self.all_submissions.search(self.keyword, limit=self.post_limit):
            serialized_post = Post(submission)
            serialized_posts.append(serialized_post)