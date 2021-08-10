import datetime

class KeywordAnalyzer:

    def run(self, reddit, keyword, subreddit_limit, post_limit):
        self.all_subreddits = reddit.subreddits
        self.all_submissions = reddit.subreddit("all")
        self.keyword = keyword
        self.subreddit_limit = subreddit_limit
        self.post_limit = post_limit
        self.collect()
        self.summarize()
    
    def collect(self):
        self.subreddits = []
        for subreddit in self.all_subreddits.search(self.keyword, limit=self.subreddit_limit):
            self.subreddits.append(subreddit)
        self.submissions = []
        for submission in self.all_submissions.search(self.keyword, limit=self.post_limit):
            self.submissions.append(submission)

    def summarize(self):
        print(f"Subreddits Collected ({len(self.subreddits)}): {self.subreddits}")
        print(f"Submissions Collected ({len(self.submissions)}): {self.submissions}")