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
import wikipedia
import nltk
from nltk import tokenize

nltk.download('punkt')

def generate_unravelled_text(input_text=None, qdepth=2, similarity=0.75, alength='summary', full_summary=""):
	"""
	generate the full unravelled text
	params:
	- input_text, the topic to be searched for
	- qdepth, the number of links to follow down the article tree
	- similarity, the cosine distance minimum for sub-topic inclusion
	- alength, the length of article to be returned - ["full","summary"]
	"""
	logging.critical("beginning unravel process for %s, qdepth=%d" % (input_text, qdepth))
	topicpage = webget(topic=input_text)
	if topicpage is not None:
		topicsummary = topicpage.summary
		links = topicpage.links
		for sentence in split_raw_text(topicsummary):
			full_summary += sentence
			full_summary += " "
			current_depth = qdepth -1
			if current_depth <= 0:
				return full_summary
			else:
				for link in links:
					if link.lower() in sentence.lower():
						if word_distance_check(link, input_text, similarity):
							full_summary += generate_unravelled_text(input_text=link, qdepth=current_depth)
							full_summary += "\n" # newline
							links.remove(link)
		return full_summary
	else:
		return full_summary

def webget(topic=None):
	"""
	get the relevant wiki summary for topic or URL
	"""
	logging.critical("webget %s commencing" % topic)
	try:
		if topic is not None:
			cg = cache_get(topic)
			if cg is None:
				topicpage = wikipedia.page(title=topic)# , preload=True) - causes open issue keyerr extlinks
				cache_set(topicpage)
				return topicpage
			else:
				return cg
	except wikipedia.exceptions.DisambiguationError as err:
		logging.info("Wikipedia disambig error: %s" % err)
		# might eventually handle this better
		return None
	except wikipedia.exceptions as err:
		logging.critical("Wikipedia error: %s" % err)
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

def cache_get(topic):
	"""
	checks the cache for topic and returns if found
	"""
	return None

def cache_set(topicpage):
	"""
	saves topic data and links to cache
	"""
	return None

def stats():
	"""
	stats for this job
	"""
	return None