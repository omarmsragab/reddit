import datetime

# class for sybmission object
class SubmissionAnalyzer:

    # "run" function that takes the url of the submission and runs "collect" and "summarize" functions 
    def run(self, reddit, submission_id, comment_limit, comment_depth):
        if 'reddit.com' in submission_id:
            self.submission = reddit.submission(url=submission_id)
        else:
            self.submission = reddit.submission(id=submission_id)
        self.submission.comments.replace_more(limit=None)
        self.comment_limit = comment_limit
        self.comment_depth = comment_depth
        self.collect()
        self.summarize()

    # "collect" function that collects data before summarizing it
    def collect(self):
        self.id = self.submission.id
        self.permalink = self.submission.permalink
        self.title = self.submission.title
        self.author = self.submission.author
        self.text = self.submission.selftext
        self.url = self.submission.url
        if self.text == '':
            if 'i.redd.it' in self.url:
                if '.gif' in self.url:
                    self.type = 'gif'
                else:
                    self.type = 'image'
            elif 'v.redd.it' in self.url or 'youtu' in self.url:
                self.type = 'video'
            else:
                self.type = 'link'                
        else:
            self.type = 'text'
        self.poll_data = []
        try:
            for option in self.submission.poll_data.options:
                current_option_data = {
                    'Option ID': option.id,
                    'Option Name': option.text
                }
                try:
                    current_option_data['Option Vote Count'] = option.vote_count
                except:
                    pass
                self.poll_data.append(current_option_data)
            self.type = 'poll'
        except:
            pass
        self.upvote_count = self.submission.score
        self.upvote_ratio = self.submission.upvote_ratio
        self.comment_count = self.submission.num_comments
        self.created_time = datetime.datetime.fromtimestamp(self.submission.created_utc)
        self.is_self = self.submission.is_self
        self.is_edited = self.submission.edited
        self.is_original_content = self.submission.is_original_content
        self.is_NSFW = self.submission.over_18
        self.is_spoiler = self.submission.spoiler
        self.flair = self.submission.link_flair_text
        self.comments = []
        self.most_upvotes_comment = ''
        self.most_upvotes = 0
        self.most_awards_comment = ''
        self.most_awards = 0
        self.ducplicates = []
        for duplicate in self.submission.duplicates():
            self.ducplicates.append(duplicate)

        def Comment_tree(current_level_comment_list, depth, collected_count):
            if len(current_level_comment_list) != 0:
                next_level_comments_list = []
                for current_level_comment in current_level_comment_list:
                    if collected_count != 0 and collected_count == self.comment_limit:
                        break
                    self.comments.append(current_level_comment)
                    if current_level_comment.score > self.most_upvotes:
                        self.most_upvotes = current_level_comment.score
                        self.most_upvotes_comment = current_level_comment.body
                    comment_awards = 0
                    for value in current_level_comment.gildings.values():
                        comment_awards += value
                    if comment_awards > self.most_awards:
                        self.most_awards = comment_awards
                        self.most_awards_comment = current_level_comment.body
                    collected_count += 1
                    next_level_comments_list.extend(current_level_comment.replies)
                if collected_count != self.comment_limit and (depth > 1 or depth < 1):
                    Comment_tree(next_level_comments_list, depth - 1, collected_count)
    
        if self.comment_depth == 0 and self.comment_limit == 0:
            self.comments = self.submission.comments.list()
            for comment in self.comments:
                if comment.score > self.most_upvotes:
                    self.most_upvotes = comment.score
                    self.most_upvotes_comment = comment.body
                comment_awards = 0
                for value in comment.gildings.values():
                    comment_awards += value
                if comment_awards > self.most_awards:
                    self.most_awards = comment_awards
                    self.most_awards_comment = comment.body
        else:
            Comment_tree(self.submission.comments, self.comment_depth, collected_count = 0)
        

    # "summarize" function that prints collected data
    def summarize(self):
        print(f"ID: {self.id}")
        print(f"Permalink: {self.permalink}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Type: {self.type}")
        if self.text != '':
            print(f"Text: {self.text}")
        if len(self.poll_data) != 0:
            print(f"Poll Data: {self.poll_data}")
        print(f"Url: {self.url}")
        print(f"Upvote Count: {self.upvote_count}")
        print(f"Upvote Ratio: {self.upvote_ratio}")
        print(f"Comment Count: {self.comment_count}")
        print(f"Created Time: {self.created_time}")
        print(f"Is Self: {self.is_self}")
        print(f"Is Edited: {self.is_edited}")
        print(f"Is Original Content: {self.is_original_content}")
        print(f"Is NSFW: {self.is_NSFW}")
        print(f"Is Spoiler: {self.is_spoiler}")
        print(f"Flair: {self.flair}")
        print(f"Comments Collected For Analyse ({len(self.comments)}): {self.comments}")
        if self.most_upvotes != 0:
            print(f"The comment with most upvotes is '{self.most_upvotes_comment}' with {self.most_upvotes} upvotes.")
        if self.most_awards != 0:
            print(f"The comment with most awards is '{self.most_awards_comment}' with {self.most_awards} awards.")
        if len(self.ducplicates) != 0:
            print(f"Duplicates: {self.ducplicates}")
        else:
            print("This submission has no duplicates.")