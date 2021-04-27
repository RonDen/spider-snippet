class ParseError(Exception):
    def __init__(self, err_url):
        super(ParseError, self).__init__()
        self.err_url = err_url

    def __str__(self):
        return "{}\n\033[0;31m解析错误！\033[0m".format(self.err_url)


class NoDataError(Exception):
    def __init__(self, err_url):
        super(NoDataError, self).__init__()
        self.err_url = err_url

    def __str__(self):
        return "{}\n\033[0;35m无数据！\033[0m".format(self.err_url)


class NotFindError404(Exception):
    def __init__(self, err_url):
        super(NotFindError404, self).__init__()
        self.err_url = err_url

    def __str__(self):
        return "{}\n\033[0;35m404错误！\033[0m".format(self.err_url)
