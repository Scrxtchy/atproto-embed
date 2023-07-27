from atproto import Client as atClient
from flask import Flask, render_template, request, redirect
from os import environ as ENV

from dotenv import load_dotenv
load_dotenv()

atp = atClient()
atp.login(ENV['bsky-usr'], ENV['bsky-pwd'])

def getPost(url):
	if url[-1] == "/":
		url = url [:-1]
	url = url.replace("post/", "")

	url = url.split("/")[-2:]
	did = atp.com.atproto.identity.resolve_handle({'handle': url[0]}).did

	uri = f"at://{did}/app.bsky.feed.post/{url[1]}"
	return atp.bsky.feed.get_posts({'uris' : [uri]}).posts[0]


app = Flask(__name__)

@app.route("/<path:url>")
def displayPost(url=None):
	if url:
		if 'bot' not in request.headers['User-Agent'].lower():
			return redirect(f"https://bsky.app/profile/{url.replace('profile/','')}")
		else:
			return render_template('post.html', post=getPost(url))
	else:
		return("Invalid", 404)

@app.route("/favico.ico")
def favicon():
	return(404)


if __name__ == "__main__":
	from pprint import pp
	url = "https://bsky.app/profile/bsky.app/post/3jt6walwmos2y"
	pp(getPost(url))