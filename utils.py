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

def generate_unravelled_text(input_text=None, url_link=None, qdepth=3, similarity=0.75, alength='summary', full_summary=[]):
	"""
	generate the full unravelled text
	params:
	- input_text, the topic to be searched for
	- qdepth, the number of links to follow down the article tree
	- similarity, the cosine distance minimum for sub-topic inclusion
	- alength, the length of article to be returned - ["full","summary"]
	"""
	topicsummary = webget(topic=input_text, url=url_link)
	if topicsummary is not None:
		# topic_sentences = split_raw_text(topicsummary)
		# full_summary = []
		for sentence in split_raw_text(topicsummary):
			parsed_sentence, links = sent_parse(sentence)
			full_summary.append(parsed_sentence)
			current_depth = qdepth -1
			if current_depth <= 0:
				return full_summary
			else:
				for link in links:
					if word_distance_check(link['word'], input_text, similarity):
						generate_unravelled_text(input_text=link['word'], url_link=link['url'], full_summary=full_summary,qdepth=current_depth)
		return full_summary
	else:
		return full_summary

def webget(topic=None, url=None):
	"""
	get the relevant wiki summary for topic or URL
	"""
	try:
		if topic is not None:
			return wikipedia.summary(topic)
	except wikipedia.exceptions as err:
		logging.critical("Wikipedia error: %s" % err)
	return None

def split_raw_text(raw):
	"""
	split raw text into sentences
	"""
	return None

def sent_parse(sentence):
	"""
	look for any links in the raw sentence, returns:
	("parsed sentence",
	[{link_word, url},
	 ..., 
	 {link_word, url}])
	"""
	return None

def word_distance_check(topic, testword, similarity):
	"""
	perform word2vec cosine distance of testword from topic
	if distance greater than similarity, return False
	"""
	return False

def cache_get(topic):
	"""
	checks the cache for topic and returns if found
	"""
	return None

def cache_set(topic, text, links):
	"""
	saves topic data and links to cache
	"""
	return None

def stats():
	"""
	stats for this job
	"""
	return None