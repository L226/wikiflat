"""
general utils for unravel project
- web get
- text parse
- hyperlink traverse
- word similarity
- text reconstruct
- job metadata
"""

def generate_unravelled_text(input_text, qdepth=3, similarity=0.75, alength='summary'):
	"""
	generate the full unravelled text
	params:
	- input_text, the topic to be searched for
	- qdepth, the number of links to follow down the article tree
	- similarity, the cosine distance minimum for sub-topic inclusion
	- alength, the length of article to be returned - ["full","summary"]
	"""
	topicsummary = webget(topic=input_text)
	if topicsummary is not None:
		topic_sentences = split_raw_text(topicsummary)

	else:
		return None

def webget(topic="", url=""):
	"""
	get the relevant wiki summary for topic or URL
	"""
	return None

def split_raw_text(raw):
	"""
	split raw text into sentences
	"""
	return None

def sent_parse(sentence):
	"""
	look for any links in the raw sentence, return list (need order preserved):
		[
		{parsed:"sentence without html",
		links:[link1,link2 ...]},
		...
		{parsed:"sentence without html",
		links:[link1,link2 ...]}
		]
	"""
	return None

def word_distance(topic, testword):
	"""
	word2vec cosine distance of testword from topic
	"""
	return 0

def stats():
	"""
	stats for this job
	"""
	return None