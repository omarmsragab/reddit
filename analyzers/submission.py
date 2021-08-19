from serializers.post import *
from serializers.comment import *
from praw.models import MoreComments

# class for sybmission object
class SubmissionAnalyzer:

    # "run" function that takes the url of the submission and runs "collect" and "summarize" functions 
    def run(self, reddit, submission_id, comment_limit, comment_depth):
        if 'reddit.com' in submission_id:
            self.submission = reddit.submission(url=submission_id)
        else:
            self.submission = reddit.submission(id=submission_id)
        self.comment_limit = comment_limit
        self.comment_depth = comment_depth
        self.collect()

    # "collect" function that collects data before summarizing it
    def collect(self):
        serialized_post = Post(self.submission)
        serialized_comments = []
        # self.most_upvotes_comment = ''
        # self.most_upvotes = 0
        # self.most_awards_comment = ''
        # self.most_awards = 0

        def Comment_tree(comment_list, next_level_comments_list, collected_count, more_comments_list):
            while True:
                if len(comment_list._comments) == 0:
                    if len(next_level_comments_list) != 0:
                        comment_list._comments.extend(next_level_comments_list)
                        next_level_comments_list.clear()
                    else:
                        break
                if collected_count != 0 and collected_count == self.comment_limit:
                    break
                current_comment = comment_list[0]
                if isinstance(current_comment, MoreComments):
                    if len(more_comments_list) == 0:
                        more_comments_list = comment_list.replace_more(limit=1)
                        if len(comment_list._comments) == 0:
                            more_comments_list.clear()
                    else:
                        more_comments = []
                        more_comments.extend(comment_list.replace_more(limit=1))
                        more_comments_list.extend(more_comments)
                        if len(comment_list._comments) == 0:
                            more_comments_list.clear()
                    if len(more_comments_list) != 0:
                        comment_list._comments.append(more_comments_list[0])
                        more_comments_list.pop(0)
                else:
                    serialized_comment = Comment(current_comment)
                    serialized_comments.append(serialized_comment)
                    collected_count += 1
                    if current_comment.depth < self.comment_depth - 1:
                        next_level_comments_list.extend(current_comment.replies)
                    comment_list._comments.pop(0)
                    # print(current_comment.id)
                    # if current_comment.score > self.most_upvotes:
                    #     self.most_upvotes = current_comment.score
                    #     self.most_upvotes_comment = current_comment.body
                    # comment_awards = 0
                    # for value in current_comment.gildings.values():
                    #     comment_awards += value
                    # if comment_awards > self.most_awards:
                    #     self.most_awards = comment_awards
                    #     self.most_awards_comment = current_comment.body
            print(f"Collected: {collected_count}")
            
        if self.comment_depth == 0 and self.comment_limit == 0:
            self.submission.comments.replace_more(limit=None)
            collected_count = 0
            for comment in self.submission.comments.list():
                serialized_comment = Comment(comment)
                serialized_comments.append(serialized_comment)
                collected_count += 1
                # if comment.score > self.most_upvotes:
                #     self.most_upvotes = comment.score
                #     self.most_upvotes_comment = comment.body
                # comment_awards = 0
                # for value in comment.gildings.values():
                #     comment_awards += value
                # if comment_awards > self.most_awards:
                #     self.most_awards = comment_awards
                #     self.most_awards_comment = comment.body
            print(collected_count)
        else:
            Comment_tree(self.submission.comments, next_level_comments_list = [], collected_count = 0, more_comments_list = [])