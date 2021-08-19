from serializers.comment import Comment
from serializers.post import Post
from serializers.user import *

class UserAnalyzer:

    def run(self, reddit, username, post_limit, comment_limit):
        self.user = reddit.redditor(username)
        self.post_limit = post_limit
        self.comment_limit = comment_limit
        self.collect()

    def collect(self):
        serialized_user = Profile(self.user)

        serialized_posts = []
        for submission in self.user.submissions.new(limit=self.post_limit):
            serialized_post = Post(submission)
            serialized_posts.append(serialized_post)
        
        serialized_comments = []
        for comment in self.user.comments.new(limit=self.post_limit):
            serialized_comment = Comment(comment)
            serialized_comments.append(serialized_comment)