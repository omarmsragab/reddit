from flatten_json import flatten


class Post():

    def __init__(self, post, scrape_source="subreddit"):
        self.scrape_source = scrape_source
        # self.trendCategory = getattr(post, '', None)
        self.objId = getattr(post, 'id', None)
        self.numComments = getattr(post, 'num_comments', None)
        self.created = getattr(post, 'created_utc', None)
        self.score = getattr(post, 'score', None)
        self.isLocked = getattr(post, 'locked', None)
        self.isStickied = getattr(post, 'stickied', None)
        self.title = getattr(post, 'title', None)
        self.author = getattr(post, 'author', None)
        self.authorId = getattr(post.author, 'id', None)
        self.domain = getattr(post, 'domain', None)
        # self.postId = getattr(post, '', None)
        self.upvoteRatio = getattr(post, 'upvote_ratio', None)
        self.viewCount = getattr(post, 'view_count', None)
        # self.goldCount = getattr(post, '', None)
        self.isArchived = getattr(post, 'archived', None)
        self.contestMode = getattr(post, 'contest_mode', None)
        self.gildings = getattr(post, 'gildings', None)
        self.suggestedSort = getattr(post, 'suggested_sort', None)
        # self.belongsTo = getattr(post, '', None)
        self.hidden = getattr(post, 'hidden', None)
        self.saved = getattr(post, 'saved', None)
        self.isGildable = getattr(post, 'can_gild', None)
        self.isMediaOnly = getattr(post, 'media_only', None)
        # self.isSponsored = getattr(post, '', None)
        self.isNSFW = getattr(post, 'over_18', None)
        self.isMeta = getattr(post, 'is_meta', None)
        self.isSpoiler = getattr(post, 'spoiler', None)
        # self.isBlank = getattr(post, '', None)
        self.sendReplies = getattr(post, 'send_replies', None)
        # self.voteState = getattr(post, '', None)
        self.permalink = getattr(post, 'permalink', None)
        self.media = getattr(post, 'media', None)
        self.numCrossposts = getattr(post, 'num_crossposts', None)
        self.isCrosspostable = getattr(post, 'is_crosspostable', None)
        # self.liveCommentsWebsocket = getattr(post, '', None)
        # self.source = getattr(post, '', None)
        self.isOriginalContent = getattr(post, 'is_original_content', None)
        self.isScoreHidden = getattr(post, 'hide_score', None)
        # self.mediaType = getattr(post, '', None)
        self.text = getattr(post, 'selftext', None)
        self.linkUrl = getattr(post, 'url', None)

        # Getting self.type
        if self.text == '':
            if 'i.redd.it' in self.linkUrl:
                if '.gif' in self.linkUrl:
                    self.type = 'gif'
                else:
                    self.type = 'image'
            elif 'v.redd.it' in self.linkUrl or 'youtu' in self.linkUrl:
                self.type = 'video'
            else:
                self.type = 'link'                
        else:
            self.type = 'text'
        try:
            poll = self.submission.poll_data
            self.type = 'poll'
        except:
            pass
        

    @classmethod
    def from_browser(cls, **kwargs):
        obj = {}
        obj['objId'] = kwargs.get("obj_id", None)
        obj['trendCategory'] = kwargs.get("trend_category", None)
        obj['numComments'] = kwargs.get("numComments", None)
        obj['created'] = kwargs.get("created", None)
        obj['score'] = kwargs.get("score", None)
        obj['isLocked'] = kwargs.get("isLocked", None)
        obj['isStickied'] = kwargs.get("isStickied", None)
        obj['title'] = kwargs.get("title", None)
        obj['author'] = kwargs.get("author", None)
        obj['authorId'] = kwargs.get("authorId", None)
        obj['domain'] = kwargs.get("domain", None)
        obj['postId'] = kwargs.get("postId", None)
        obj['upvoteRatio'] = kwargs.get("upvoteRatio", None)
        obj['viewCount'] = kwargs.get("viewCount", None)
        obj['goldCount'] = kwargs.get("goldCount", None)
        obj['isArchived'] = kwargs.get("isArchived", None)
        obj['contestMode'] = kwargs.get("contestMode", None)
        obj['gildings'] = kwargs.get("gildings", None)
        obj['suggestedSort'] = kwargs.get("suggestedSort", None)
        obj['belongsTo'] = kwargs.get("belongsTo", None)
        obj['hidden'] = kwargs.get("hidden", None)
        obj['saved'] = kwargs.get("saved", None)
        obj['isGildable'] = kwargs.get("isGildable", None)
        obj['isMediaOnly'] = kwargs.get("isMediaOnly", None)
        obj['isSponsored'] = kwargs.get("isSponsored", None)
        obj['isNSFW'] = kwargs.get("isNSFW", None)
        obj['isMeta'] = kwargs.get("isMeta", None)
        obj['isSpoiler'] = kwargs.get("isSpoiler", None)
        obj['isBlank'] = kwargs.get("isBlank", None)
        obj['sendReplies'] = kwargs.get("sendReplies", None)
        obj['voteState'] = kwargs.get("voteState", None)
        obj['permalink'] = kwargs.get("permalink", None)
        obj['numCrossposts'] = kwargs.get("numCrossposts", None)
        obj['isCrosspostable'] = kwargs.get("isCrosspostable", None)
        obj['liveCommentsWebsocket'] = kwargs.get("liveCommentsWebsocket", None)
        obj['isOriginalContent'] = kwargs.get("isOriginalContent", None)
        obj['isScoreHidden'] = kwargs.get("isScoreHidden", None)
        obj['type'] = kwargs.get("type", "post")

        media = obj['media'] = kwargs.get("media", {})
        if media is None:
            media = {}
        obj['mediaType'] = media.get("type", None)
        if obj['mediaType'] == 'rtjson':
            text = reddit_rtf_to_string(media.get("richtextContent", ''))
            obj['text'] = text if text else None

        source = obj['source'] = kwargs.get("source", {})
        if source is None:
            source = {}
        obj['linkUrl'] = source.get("url", None)

        return cls(**obj)

    @classmethod
    def from_pushshift(cls, **kwargs):
        id = f't3_{kwargs.get("id", None)}'
        obj = {}

        obj['objId'] = id
        obj['trendCategory'] = kwargs.get("trend_category", 'new')
        obj['numComments'] = kwargs.get("num_comments", None)
        obj['created'] = kwargs.get("created_utc", None)
        obj['score'] = kwargs.get("score", None)
        obj['isLocked'] = kwargs.get("locked", None)
        obj['isStickied'] = kwargs.get("stickied", None)
        obj['title'] = kwargs.get("title", None)
        obj['author'] = kwargs.get("author", None)
        obj['authorId'] = kwargs.get("author_fullname", None)
        obj['domain'] = kwargs.get("domain", None)
        obj['postId'] = id
        obj['upvoteRatio'] = kwargs.get("upvote_ratio", None)
        # obj['viewCount'] = kwargs.get("viewCount", 0)
        # obj['goldCount'] = kwargs.get("goldCount", 0)
        # obj['isArchived'] = kwargs.get("isArchived", None)
        obj['contestMode'] = kwargs.get("contest_mode", None)
        obj['gildings'] = kwargs.get("gildings", None)
        obj['suggestedSort'] = kwargs.get("suggested_sort", None)
        # obj['belongsTo'] = kwargs.get("belongsTo", {})
        # obj['hidden'] = kwargs.get("hidden", None)
        # obj['saved'] = kwargs.get("saved", None)
        obj['isGildable'] = kwargs.get("can_gild", None)
        # obj['isMediaOnly'] = kwargs.get("isMediaOnly", None)
        # obj['isSponsored'] = kwargs.get("isSponsored", None)
        obj['isNSFW'] = kwargs.get("over_18", None)
        obj['isMeta'] = kwargs.get("is_meta", None)
        obj['isSpoiler'] = kwargs.get("spoiler", None)
        # obj['isBlank'] = kwargs.get("isBlank", None)
        obj['sendReplies'] = kwargs.get("send_replies", None)
        # obj['voteState'] = kwargs.get("voteState", 0)
        obj['permalink'] = kwargs.get("full_link", None)
        obj['numCrossposts'] = kwargs.get("num_crossposts", None)
        obj['isCrosspostable'] = kwargs.get("is_crosspostable", None)
        # obj['liveCommentsWebsocket'] = kwargs.get("liveCommentsWebsocket", None)
        obj['isOriginalContent'] = kwargs.get("is_original_content", None)
        # obj['contentCategories'] = kwargs.get("contentCategories", None)
        # obj['isScoreHidden'] = kwargs.get("isScoreHidden", None)
        obj['type'] = kwargs.get("type", 'post')

        obj['text'] = kwargs.get("selftext", None)
        if obj['text'] == "":
            obj['text'] = None
        obj['linkUrl'] = kwargs.get("url", None)

        return cls(**obj)

    def to_dict(self, **kwargs):
        style = kwargs.get('style', 'rest')

        if self.objId is None:
            return None

        data = self.__dict__
        scrape_source = data.pop('scrape_source', None)

        if style == 'rest':
            return {
                "_id": f"redditPost_2_{self.objId.upper()}",
                "meta": {
                    "retrieved_activities": True,
                    "scrape_source": scrape_source
                },
                "data": data
            }

        elif style == 'jsonapi':
            return {
                "_id": f"redditPost_2_{self.objId.upper()}",
                "type": "post",
                "attributes": data,
                "meta": {
                        "retrieved_activities": True,
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