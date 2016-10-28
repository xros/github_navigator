#!/usr/bin/env python2
# coding: utf-8
import os
import json
import tornado
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.template

from tornado.options import define, options
import urllib2
import urllib


define("port", default=9876, help="run on the given port", type=int)

ROOT_PATH = os.path.dirname(__file__)
tmp_file = os.path.join(ROOT_PATH, "template.html")


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        super(BaseHandler, self).initialize()

    def write_error(self, status_code, **kwargs):
        if status_code==500:
            self.write("""<h1>Internal Error</h1>
                        <h2>URI or Parameter invalid</h2>
                    
                        <p>
                            Input example in URI:
                                /navigator?search_term=example
                        </p>
                       """)
            return
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)


def insertionSortedByCreatedAt(the_list):
	# the_list is a list of dict, sorting by its value "created_at"

    for i in range(1, len(the_list)):
        tmp = the_list[i]           # tmp is a dict obj
        k = i

        # we only want biggest at array front
        while k > 0 and tmp["created_at"] > the_list[k-1]["created_at"]:
            the_list[k] = the_list[k-1]
            the_list[k-1] = tmp
            k = k - 1
        the_list[k] = tmp
    return the_list


# Github latest 5 repo
class GetLatest5Repo(BaseHandler):
    def get(self, *args, **kwargs):
        # get parameters
        search_term = self.get_argument("search_term", default=None, strip=False)
        if search_term is None:
            self.write("""<h1>Parameter invalid</h1>
                        <p>
                            Input example in URI:
                                /navigator?search_term=example
                            <br>
                            search_term cannot be empty
                            </br>
                        </p>
                       """)
            return

        # GitHub API v3: Get the latest 5 github repo
        # TODO to test if sorted correctly:                         Passed
        results = []
        url = "https://api.github.com/search/repositories?q=" + search_term + "&sort=created&order=desc"
        # url = "https://api.github.com/search/repositories?q=" + search_term + "&sort=updated&order=desc"
        request = urllib.urlopen(url)
        r = request.readlines()
        gotten = r[0]
        gotten = json.loads(gotten)


        items_sorted_by_created_at = []


        #####
        # GitHub API v3 does not have options for sorting repo results by created data
        # We have to do it locally
        ####

        # do the insertion sorting sorted by its dict value of "created_at" decreasing
        gotten["items"] = insertionSortedByCreatedAt(gotten["items"])


        # we only need top 5 results
        total_count = gotten["total_count"]

        if total_count >= 5:
            for i in range(5):
                results.append(
                    {
                        "search_term": search_term,
                        # "total_count" : gotten["total_count"],
                        "repository_name" : gotten["items"][i]["name"],
                        "created_at" : gotten["items"][i]["created_at"],
                        "owner_url" : gotten["items"][i]["owner"]["html_url"],
                        "avatar_url" : gotten["items"][i]["owner"]["avatar_url"],
                        "owner_login" : gotten["items"][i]["owner"]["login"],
                        # cmt_url looks like: https://api.github.com/repos/xros/jsonpyes/commits{/sha} , need to remove {/sha} in the URL
                        "cmt_url" : gotten["items"][i]["commits_url"].replace("{/sha}",""),
                        "sha": "",
                        "commit_message": "",
                        "commit_author_name": "",
                    
                    }
                )
        else:
            for i in range(total_count):
                results.append(
                    {
                        "search_term": search_term,
                        # "total_count" : gotten["total_count"],
                        "repository_name" : gotten["items"][i]["name"],
                        "created_at" : gotten["items"][i]["created_at"],
                        "owner_url" : gotten["items"][i]["owner"]["html_url"],
                        "avatar_url" : gotten["items"][i]["owner"]["avatar_url"],
                        "owner_login" : gotten["items"][i]["owner"]["login"],
                        # cmt_url looks like: https://api.github.com/repos/xros/jsonpyes/commits{/sha} , need to remove {/sha} in the URL
                        "cmt_url" : gotten["items"][i]["commits_url"].replace("{/sha}",""),
                        "sha": "",
                        "commit_message": "",
                        "commit_author_name": "",
                    }
                )

        # mappings for the 1st one result e.g.
        # repository_name = gotten["items"][0]["name"]
        # created_at = gotten["items"][0]["created_at"]
        # owner_url = gotten["items"][0]["owner"]["html_url"]
        # avatar_url = gotten["items"][0]["owner"]["avatar_url"]
        # owner_login = gotten["items"][0]["owner"]["login"]

        for m in results:
            request = urllib.urlopen(m["cmt_url"])
            r = request.readlines()
            # only use the latest 1 commit
            cmt_gotten = r[0]
            # print(type(cmt_gotten))
            cmt_gotten = json.loads(cmt_gotten)

            # print(cmt_gotten)

            sha = cmt_gotten[0]["sha"]
            # print(sha)
            commit_message = cmt_gotten[0]["commit"]["message"]
            commit_author_name = cmt_gotten[0]["commit"]["author"]["name"]

            results[results.index(m)]["sha"] = sha
            results[results.index(m)]["commit_message"] = commit_message
            results[results.index(m)]["commit_author_name"] = commit_author_name
            

        # print(results)

        loader = tornado.template.Loader(root_directory=ROOT_PATH)

        t = loader.load("template.html")

        html_content = t.generate(results=results)
        
        self.write(html_content)
        return


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/navigator", GetLatest5Repo),                           # Testing : Passed


            #(r"/update/dealer/profile", UpdateProfileHandler)
            #(r"")
        ]

        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),no_keep_alive=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


