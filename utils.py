"""
general utils for unravel project
- web get
- text parse
- hyperlink traverse
- word similarity
- text reconstruct
- job metadata
"""
import os
import logging
import logging.config
import redis
import HTMLParser
import wikipedia
import nltk
from nltk import tokenize
try:
	import cPickle as pickle
except:
	import pickle

logging.config.fileConfig('log.conf')
logger = logging.getLogger(__name__)

nltk.download('punkt')

def gen_disp_text(input_text=None):
	"""
	generate html safe text for display
	"""
	processed_text, siteurl = generate_unravelled_text(input_text=input_text, full_summary=[])
	# disp_text = processed_text.encode('ascii', 'xmlcharrefreplace')
	html_parser = HTMLParser.HTMLParser()
	disp_text = ""
	for row in processed_text:
		disp_text += html_parser.unescape(row)
		# disp_text += "<br />"
	return disp_text, siteurl

def generate_unravelled_text(input_text=None, qdepth=2, similarity=0.75, alength='summary', full_summary=[], prevlinked=[]):
	"""
	generate the full unravelled text
	params:
	- input_text, the topic to be searched for
	- qdepth, the number of links to follow down the article tree
	- similarity, the cosine distance minimum for sub-topic inclusion
	- alength, the length of article to be returned - ["full","summary"]
	"""
	logger.info("beginning unravel process for %s, qdepth=%d" % (input_text, qdepth))
	topicpage = webget(topic=input_text)
	if topicpage is not None:
		siteurl = topicpage.url
		prevlinked.append(input_text.lower())
		topicsummary = topicpage.summary
		links = topicpage.links
		for sentence in split_raw_text(topicsummary):
			full_summary.extend([sentence, " "])
			# tmp_summ += " "
			current_depth = qdepth -1
			if current_depth <= 0:
				return [sentence, "<br /><br />"], siteurl
			else:
				for link in links:
					if link.lower() in sentence.lower() and link.lower() not in prevlinked:
					# doesn't get non identical link text, link value
						if word_distance_check(link, input_text, similarity):
							prevlinked.append(link.lower())
							full_summary.extend(generate_unravelled_text(input_text=link, qdepth=current_depth, full_summary=[], prevlinked=prevlinked)[0])
						links.remove(link)
		return full_summary, siteurl
	else:
		return full_summary, None

def webget(topic=None):
	"""
	get the relevant wiki summary for topic or URL
	"""
	logger.debug("webget %s commencing" % topic)
	try:
		if topic is not None:
			cg = cache_get(topic)
			if cg is None:
				logging.info("failed to find cache for %s" % topic)
				topicpage = wikipedia.page(title=topic, preload=True) # preload causes open issue keyerr extlinks
				logging.info("setting cache for %s" % topic)
				cache_set(topic, topicpage)
				return topicpage
			else:
				logging.info("found cache for %s" % topic)
				return cg
	except wikipedia.exceptions.DisambiguationError as err:
		logger.info("Wikipedia disambig error: %s" % err)
		# might eventually handle this better
		return None
	except wikipedia.exceptions as err:
		logger.critical("Wikipedia error: %s" % err)
	return None

def split_raw_text(raw):
	"""
	split raw text into sentences
	"""
	return tokenize.sent_tokenize(raw)

def word_distance_check(topic, testword, similarity):
	"""
	perform word2vec cosine distance of testword from topic
	if distance greater than similarity, return False
	"""
	return True

def redis_connect():
	"""
	look for remote or local redis cache and return connection object if found
	"""
	if os.environ.get("REDIS_URL", None) is not None:
		return redis.from_url(os.environ.get("REDIS_URL"))
	elif os.environ.get("REDIS_PORT", None) is not None: # easy check for docker-compose env
		return redis.StrictRedis(host='redis', port=os.environ['REDIS_PORT'])
	else:
		return None

def cache_get(topic):
	"""
	checks the cache for topic and returns if found
	"""
	try:
		r = redis_connect()
		if r is not None:
			logger.info("performing cache lookup for %s" % topic)
			topicget = r.get(topic)
			if topicget is not None:
				return pickle.loads(topicget)
	except ConnectionError as err:
		logger.critical("Redis ConnectionError: %s" % err)
	return None

def cache_set(topic, topicpage):
	"""
	saves topic data and links to cache
	"""
	try:
		r = redis_connect()
		if r is not None:
			if r.set(name=topic, value=pickle.dumps(topicpage), ex=21600): # 6hr expiry
				logging.info('successfully saved %s to cache' % topic)
		else:
			return None
	except ConnectionError as err:
		logger.critical("Redis ConnectionError: %s" % err)
	return None

def stats():
	"""
	stats for this job
	"""
	return None