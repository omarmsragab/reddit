import json
import praw
from analyzers.keyword import *
from analyzers.submission import *
from analyzers.subreddit import *
from analyzers.user import *

# main function
def main():
    # setting up praw to use it later
    f = open('credentials.json')
    client_info = json.load(f)
    reddit = praw.Reddit(
        client_id = client_info["client_id"],
        client_secret = client_info["client_secret"],
        user_agent = "user_agent.0.1.0",
    )
    while True:
        # asking the user to choose job to do, either subreddit or submission/post, and then running the job
        job_type = input("Enter Job Type(Search/Subreddit/Submission/User): ")
        if job_type.lower() == 'search' or job_type.lower() == 'keyword':
            keyword = input("Enter Keyword: ")
            while True:
                subreddit_limit = input("Enter number of subreddits to collect (type '0' for all subreddits): ")
                if subreddit_limit.isnumeric():
                    subreddit_limit = int(subreddit_limit)
                    if subreddit_limit < 0:
                            print("Value must be greater than or equal to 0, please try again.")
                    elif subreddit_limit == 0:
                        subreddit_limit = None
                        break
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            while True:
                post_limit = input("Enter number of submissions to collect (type '0' for all submissions): ")
                if post_limit.isnumeric():
                    post_limit = int(post_limit)
                    if post_limit < 0:
                            print("Value must be greater than or equal to 0, please try again.")
                    elif post_limit == 0:
                        post_limit = None
                        break
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            user = KeywordAnalyzer()
            user.run(reddit, keyword, subreddit_limit, post_limit)
            break
        elif job_type.lower() == 'subreddit':
            sr_name = input("Enter subreddit Name: ")
            while True:
                post_limit = input("Enter number of submissions to analyse (type '0' for all submissions): ")
                if post_limit.isnumeric():
                    post_limit = int(post_limit)
                    if post_limit < 0:
                        print("Value must be greater than or equal to 0, please try again.")
                    elif post_limit == 0:
                        post_limit = None
                        break
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            while True:
                sort_by = input("Enter type of submission sorting (New/Rising/Controversial/Top/Gilded): ")
                if sort_by.lower() in ['new', 'rising', 'controversial', 'top', 'gilded']:
                    sort_by = sort_by.lower()
                    sort_by_top_range = ''
                    if sort_by == 'top':
                        while True:
                            sort_by_top_range = input("Enter time range for 'top' sorting (Hour/Day/Week/Month/Year/All): ")
                            if sort_by_top_range.lower() in ['hour', 'day', 'week', 'month', 'year', 'all']:
                                sort_by_top_range = sort_by_top_range.lower()
                                break
                            else:
                                print("Value not valid, please try again.")
                    break
                else:
                    print("Value not valid, please try again.")
            subreddit = SubredditAnalyzer()
            subreddit.run(reddit, sr_name, post_limit, sort_by, sort_by_top_range)
            break
        elif job_type.lower() == 'submission' or job_type.lower() == 'post':
            submission_id = input("Enter submission url or ID: ")
            while True:
                comment_limit = input("Enter number of comments to analyse (type '0' for all comments): ")
                if comment_limit.isnumeric():
                    comment_limit = int(comment_limit)
                    if comment_limit < 0:
                            print("Value must be greater than or equal to 0, please try again.")
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            while True:
                comment_depth = input("Enter depth of comments to analyse (type '0' for all comments): ")
                if comment_depth.isnumeric():
                    comment_depth = int(comment_depth)
                    if comment_depth < 0:
                        print("Value must be greater than or equal to 0, please try again.")
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            submission = SubmissionAnalyzer()
            submission.run(reddit, submission_id, comment_limit, comment_depth)
            break
        elif job_type.lower() == 'user' or job_type.lower() == 'redditor':
            username = input("Enter redditor username: ")
            while True:
                post_limit = input("Enter number of submissions to analyse (type '0' for all submissions): ")
                if post_limit.isnumeric():
                    post_limit = int(post_limit)
                    if post_limit < 0:
                            print("Value must be greater than or equal to 0, please try again.")
                    elif post_limit == 0:
                        post_limit = None
                        break
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            while True:
                comment_limit = input("Enter number of comments to analyse (type '0' for all comments): ")
                if comment_limit.isnumeric():
                    comment_limit = int(comment_limit)
                    if comment_limit < 0:
                            print("Value must be greater than or equal to 0, please try again.")
                    elif comment_limit == 0:
                        comment_limit = None
                        break
                    else:
                        break
                else:
                    print("Value must be a number greater than or equal to 0, please try again.")
            user = UserAnalyzer()
            user.run(reddit, username, post_limit, comment_limit)
            break
        else:
            print("Job type not defined, please try again.") # reasking the user to choose the job if choice  isn't clear
if __name__ == '__main__':    
    main()