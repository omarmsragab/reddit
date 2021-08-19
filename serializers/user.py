class Profile():

    def __init__(self, user):

        # self.acceptChats = getattr(user, '', None)
        # self.acceptPms = getattr(user, '', None)
        self.awardeeKarma = getattr(user, 'awardee_karma', None)
        self.awarderKarma = getattr(user, 'awarder_karma', None)
        self.commentKarma = getattr(user, 'comment_karma', None)
        # self.postKarma = getattr(user, '', None)
        # self.publicDescription = getattr(user, '', None)
        self.totalKarma = getattr(user, 'total_karma', None)
        # self.userIsSubscriber = getattr(user, '', None)
        # self.communityIcon = getattr(user, '', None)
        # self.displayText = getattr(user, '', None)
        self.icon = getattr(user, 'icon_img', None)
        self.objId = getattr(user, 'id', None)
        # self.isQuarantined = getattr(user, '', None)
        self.name = getattr(user, 'name', None)
        # self.primaryColor = getattr(user, '', None)
        # self.subscribers = getattr(user, '', None)
        # self.title = getattr(user, '', None)
        # self.type = getattr(user, '', None)
        # self.url = getattr(user, '', None)



    def to_dict(self, **kwargs):
        style = kwargs.get('style', 'rest')

        if self.objId is None:
            return None

        if style == 'rest':
            return {
                "_id": f"redditUser_2_{self.objId.upper()}",
                "meta": None,
                "data": self.__dict__
            }

        elif style == 'jsonapi':
            return {
                "_id": f"redditUser_2_{self.objId.upper()}",
                "type": "user",
                "attributes": self.__dict__,
                "meta": {}
            }