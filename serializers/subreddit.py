import datetime

class Subreddit():

    def __init__(self, subreddit, is_keyword_search=False):

        self.is_keyword_search = is_keyword_search

        if is_keyword_search:
            self.advertiserCategory = getattr(subreddit, 'advertiser_category', None)
            self.publicDescription = getattr(subreddit, 'public_description', None)
            self.subscribers = getattr(subreddit, 'subscribers', None)
            self.created = getattr(subreddit, 'created_utc', None)
            self.objId = getattr(subreddit, 'id', None)
            self.type = getattr(subreddit, 'subreddit_type', None)
            self.isNSFW = getattr(subreddit, 'over18', None)
            self.name = getattr(subreddit, 'name', None)
            self.url = getattr(subreddit, 'url', None)
            self.title = getattr(subreddit, 'title', None)
            self.icon = getattr(subreddit, 'icon_img', None)

        else:
            self.objId = getattr(subreddit, 'id', None)
            self.allowChatPostCreation = getattr(subreddit, 'allow_chat_post_creation', None)
            self.isChatPostFeatureEnabled = getattr(subreddit, 'is_chat_post_feature_enabled', None)
            #self.displayText = getattr(subreddit, '', None)
            self.type = getattr(subreddit, 'subreddit_type', None)
            self.isQuarantined = getattr(subreddit, 'quarantine', None)
            self.isNSFW = getattr(subreddit, 'over18', None)
            self.name = getattr(subreddit, 'name', None)
            self.url = getattr(subreddit, 'url', None)
            self.title = getattr(subreddit, 'title', None)
            self.icon = getattr(subreddit, 'icon_img', None)
            self.whitelistStatus = getattr(subreddit, 'whitelist_status', None)
            self.wls = getattr(subreddit, 'wls', None)
            self.communityIcon = getattr(subreddit, 'community_icon', None)
            self.primaryColor = getattr(subreddit, 'primary_color', None)
            self.subscribers = getattr(subreddit, 'subscribers', None)
            self.freeFormReports = getattr(subreddit, 'free_form_reports', None)
            self.isEnrolledInNewModmail = getattr(subreddit, 'is_enrolled_in_new_modmail', None)
            self.accountsActive = getattr(subreddit, 'accounts_active', None)
            self.usingNewModmail = getattr(subreddit, 'is_enrolled_in_new_modmail', None)
            self.publicDescription = getattr(subreddit, 'public_description', None)
            self.showMedia = getattr(subreddit, 'show_media', None)
            self.userIsSubscriber = getattr(subreddit, 'user_is_subscriber', None)
            self.userIsContributor = getattr(subreddit, 'user_is_contributor', None)
            self.restrictPosting = getattr(subreddit, 'restrict_posting', None)
            self.restrictCommenting = getattr(subreddit, 'restrict_commenting', None)
            self.disableContributorRequests = getattr(subreddit, 'disable_contributor_requests', None)
            self.submitLinkLabel = getattr(subreddit, 'submit_link_label', None)
            self.submitTextLabel = getattr(subreddit, 'submit_text_label', None)
            self.created = getattr(subreddit, 'created_utc', None)
            self.userIsBanned = getattr(subreddit, 'user_is_banned', None)
            self.emojisEnabled = getattr(subreddit, 'emojis_enabled', None)
            #self.contentCategory = getattr(subreddit, '', None)
            self.allOriginalContent = getattr(subreddit, 'all_original_content', None)
            self.originalContentTagEnabled = getattr(subreddit, 'original_content_tag_enabled', None)
            #self.hasExternalAccount = getattr(subreddit, '', None)
            self.isCrosspostableSubreddit = getattr(subreddit, 'is_crosspostable_subreddit', None)
            self.allowedPostTypes = []
            if subreddit.allow_images == True:
                self.allowedPostTypes.append('Image')
            if subreddit.allow_videos == True:
                self.allowedPostTypes.append('Video')
            if subreddit.allow_polls == True:
                self.allowedPostTypes.append('Poll')
            if subreddit.allow_videogifs == True:
                self.allowedPostTypes.append('Gif')
            if subreddit.allow_chat_post_creation == True:
                self.allowedPostTypes.append('Chat Post Creation')
            if subreddit.allow_discovery == True:
                self.allowedPostTypes.append('Discovery')
            if subreddit.allow_galleries == True:
                self.allowedPostTypes.append('Galleries')
            if subreddit.allow_predictions == True:
                self.allowedPostTypes.append('Predictions')
            if subreddit.allow_predictions_tournament == True:
                self.allowedPostTypes.append('Predictions Tournaments')



    def to_dict(self, **kwargs):
        style = kwargs.get("args", {}).get('style', 'rest')

        if self.objId is None:
            return None

        if style == 'rest':
            if self.is_keyword_search:
                return {
                    "_id": f"keywordSearch_2_{self.objId.upper()}",
                    "meta": None,
                    "data":self.__dict__
                }

            else:
                return {
                    "_id": f"redditSubreddit_2_{self.objId.upper()}",
                    "meta": None,
                    "data":self.__dict__
                }
        elif style =='jsonapi':
            if self.is_keyword_search:
                return {
                    "_id": f"keywordSearch_2_{self.objId.upper()}",
                    "type": "keyword",
                    "attributes": self.__dict__,
                    "meta": {}
                }
            else:
                return {
                    "_id": f"redditSubreddit_2_{self.objId.upper()}",
                    "type": "subreddit",
                    "attributes": self.__dict__,
                    "meta": {}
                }