# Wikiflat
#### (né Unravel)
A small app to flatten out in depth wikipedia topic summaries into a single article.

When reading deep (usually technical) topics on wikipedia I sometimes find it tedious to follow 'rabbit holes' of hyperlinks from the original article. The purpose of this app is to 'flatten' the tree structure of these page hyperlinks into a longer, denser article that allows the reader to very quickly get a good overview of a given topic without having to click down through many sub-topics.

To prevent the summary article from diverging down branches that have only cursory relevance to the original topic under investigation, this app uses word2vec to perform cosine similarity between the potential branch link name and the original topic name. If the distance is too great (default: <= 0.75) then that branch is not traversed. Additionally, the depth of the branch search (i.e. number of consecutive nodes followed down a particular branch) is limited to 2 by default.

## Deployment
- [Demo App (Heroku)](http://wikiflat.herokuapp.com)

### Local Development
- Run with docker-compose to provision a local redis cache for the app
```
$ docker-compose build
$ docker-compose up
```

- Run with Docker
```
$ docker build -it wikiflat .
$ docker run -p 80:8000 -it wikiflat
```

- Run with python
```
$ python application.py
```
## Contribute
My CSS skills suck, please help. Feel free to help out with any of the TODOs, or raise an issue on github.

### TODO
- word2vec word comparison
- proper CSS/layout/styling
- interactive generator params (similarity, query depth etc)
- link traversal via html hyperlinks (matches non identical link/link text)
	- currently 2 word links, unmatched links do not get traversed by the algorithm
- full page summaries