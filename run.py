from analyzers.submission import *
from analyzers.subreddit import *

# main function
def main():
    while True:
        # asking the user to choose job to do, either subreddit or submission/post, and then running the job
        job_type = input("Enter Job Type(Subreddit/Submission): ")
        if job_type.lower() == 'subreddit':
            sr_name = input("Enter subreddit Name: ")
            while True:
                limit = input("Enter number of submissions to analyse (leave blank for unlimited): ")
                if limit.isnumeric():
                    limit = int(limit)
                    if limit < 0:
                        print("Value must be a positive number or blank, please try again.")
                    else:
                        break
                elif limit == '':
                    break
                else:
                    print("Value must be a positive number or blank, please try again.")
            subreddit = SubredditAnalyser()
            subreddit.run(sr_name, limit)
            break
        elif job_type.lower() == 'submission' or job_type.lower() == 'post':
            submission_url = input("Enter submission/post url: ")
            while True:
                limit = input("Enter number of comments to analyse (leave blank for unlimited): ")
                if limit.isnumeric():
                    limit = int(limit)
                    if limit < 0:
                            print("Value must be a positive number or blank, please try again.")
                    else:
                        break
                elif limit == '':
                    break
                else:
                    print("Value must be a positive number or blank, please try again.")
            while True:
                depth = input("Enter depth of comments to analyse (type '0' for all comments): ")
                if depth.isnumeric():
                    depth = int(depth)
                    if depth < 0:
                        print("Value must be a positive number, please try again.")
                    else:
                        break
                else:
                    print("Value must be a positive number, please try again.")
            submission = SubmissionAnalyser()
            submission.run(submission_url, limit, depth)
            break
        else:
            print("Job type not defined, please try again.") # reasking the user to choose the job if choice  isn't clear
if __name__ == '__main__':    
    main()