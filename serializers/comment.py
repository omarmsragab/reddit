from flatten_json import flatten
import datetime

class Comment():

    def __init__(self, comment, scrape_source="post", retrieved_user = False):

        self.scrape_source = scrape_source
        self.retrieved_user = retrieved_user
        # self.trendCategory = getattr(comment, '', None)

        self.objId = getattr(comment, 'id', None)
        self.author = getattr(comment, 'author', None)
        self.authorId = getattr(comment.author, 'id', None)
        self.collapsed = getattr(comment, 'collapsed', None)
        self.collapsedReason = getattr(comment, 'collapsed_reason', None)
        self.collapsedBecauseCrowdControl = getattr(comment, 'collapsed_because_crowd_control', None)
        self.created = getattr(comment, 'created_utc', None)
        # self.deletedBy = getattr(comment, '', None)
        # self.distinguishType = getattr(comment, '', None)
        # self.editedAt = getattr(comment, '', None)
        self.gildings = getattr(comment, 'gildings', None)
        # self.goldCount = getattr(comment, '', None)
        # self.isAdmin = getattr(comment, '', None)
        # self.isDeleted = getattr(comment, '', None)
        self.isGildable = getattr(comment, 'can_gild', None)
        self.isLocked = getattr(comment, 'locked', None)
        # self.isMod = getattr(comment, '', None)
        self.isOp = getattr(comment, 'is_submitter', None)
        self.isSaved = getattr(comment, 'saved', None)
        self.isStickied = getattr(comment, 'stickied', None)
        self.isScoreHidden = getattr(comment, 'score_hidden', None)
        self.parentId = getattr(comment, 'parent_id', None)
        self.permalink = getattr(comment, 'permalink', None)
        self.postAuthor = getattr(comment.submission, 'author', None)
        self.postId = getattr(comment.submission, 'id', None)
        self.postTitle = getattr(comment.submission, 'title', None)
        self.score = getattr(comment, 'score', None)
        self.sendReplies = getattr(comment, 'send_replies', None)
        self.subredditId = getattr(comment, 'subreddit_id', None)
        # self.voteState = getattr(comment, '', None)
        # self.media = getattr(comment, '', None)
        # self.profileImage = getattr(comment, '', None)
        self.type = getattr(comment, 'comment_type', None)

        # if self.media and self.media.get("type", None) == 'rtjson':
        #     self.text = reddit_rtf_to_string(self.media.get("richtextContent", ''))

    def to_dict(self, source="subreddit", **kwargs):
        style = kwargs.get('style', 'rest')

        if self.objId is None:
            return None

        data = self.__dict__
        scrape_source = data.pop('scrape_source', None)

        if style == 'rest':
            return {
                "_id": f"redditComment_2_{self.objId.upper()}",
                "meta": {
                    "retrieved_user": False,
                    "scrape_source": scrape_source
                },
                "data": data
            }

        elif style == 'jsonapi':
            return {
                "_id": f"redditComment_2_{self.objId.upper()}",
                "type": "comment",
                "attributes": data,
                "meta": {
                        "retrieved_user": False,
                        "scrape_source": scrape_source
                }
            }

def reddit_rtf_to_string(rtf):
    """
    Converts the reddit rtf format for posts into a readable string
    """
    rtf_text = flatten(rtf)
    text = ''
    for key in rtf_text:
        if key.endswith("_t"):
            text += ' ' + rtf_text[key]
    return text