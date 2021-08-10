import datetime

class UserAnalyzer:

    def run(self, reddit, username, post_limit, comment_limit):
        self.user = reddit.redditor(username)
        self.post_limit = post_limit
        self.comment_limit = comment_limit
        self.collect()
        self.summarize()
    
    def collect(self):
        self.id = self.user.id
        self.name = self.user.name
        self.avatar = self.user.icon_img
        self.created_time = datetime.datetime.fromtimestamp(self.user.created_utc)
        self.has_verified_email = self.user.has_verified_email
        self.is_employee = self.user.is_employee
        self.is_mod = self.user.is_mod
        self.is_gold = self.user.is_gold
        try:
            self.is_suspended = self.user.is_suspended
        except:
            pass
        self.comment_karma = self.user.comment_karma
        self.link_karma = self.user.link_karma
        self.subreddit = {
            'Subreddit Name': self.user.subreddit["name"],
            'Subreddit Title': self.user.subreddit["title"],
            'Banner Image': self.user.subreddit['banner_img'],
            'Public Description': self.user.subreddit["public_description"],
            'Subscriber Count': self.user.subreddit["subscribers"],
            'Is NSFW': self.user.subreddit["over_18"]
        }

        self.submissions = []
        for submission in self.user.submissions.new(limit=self.post_limit):
            self.submissions.append(submission)
        self.comments = []
        for comment in self.user.comments.new(limit=self.post_limit):
            self.comments.append(comment)

    def summarize(self):
        print(f"ID: {self.id}")
        print(f"Username: {self.name}")
        print(f"Avatar: {self.avatar}")
        print(f"Created Time: {self.created_time}")
        print(f"Has Verified Email: {self.has_verified_email}")
        print(f"Is Employee: {self.is_employee}")
        print(f"Is Mod: {self.is_mod}")
        print(f"Has Reddit Premium: {self.is_gold}")
        try:
            print(f"Is Suspended: {self.is_suspended}")
        except:
            pass
        print(f"Comment Karma: {self.comment_karma}")
        print(f"Link Karma: {self.link_karma}")
        print(f"User Created Subreddit: {self.subreddit}")
        print(f"User's Most Recent Submissions: {self.submissions}")
        print(f"User's Most Recent Comment: {self.comments}")