from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from neo4j import GraphDatabase

def extract_keywords(input_string):
    words = word_tokenize(input_string)
    stop_words = set(stopwords.words("english"))
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", "'", '"', ",", ".", "/", "<", ">", "?", "|", "`", "~"]
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word not in symbols]
    keywords = list(set(filtered_words))
    return keywords

def search_mongodb(s):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    try:
        fields_to_index = ["videoInfo.snippet.title", "videoInfo.snippet.tags", "videoInfo.snippet.description"]
        custom_weights = {
            "videoInfo.snippet.title": 3,
            "videoInfo.snippet.tags": 1,
            "videoInfo.snippet.description": 1
        }
        index_name = "text_index"
        index_keys = [(field, "text") for field in fields_to_index]
        collection.create_index(index_keys, name=index_name, weights=custom_weights)
    except Exception as e:
        collection.drop_index(index_name)
        collection.create_index(index_keys, name=index_name, weights=custom_weights)

    keywords = extract_keywords(s)
    query = {
        "$text": {
            "$search": " ".join(keywords),
            "$caseSensitive": False
        }
    }
    projection = {
        "score": {"$meta": "textScore"}
    }
    sort = [("score", {"$meta": "textScore"})]
    results = collection.find(query, projection).sort(sort)
    res = []
    for x in results:
        temp = {
            "_id": x.get("_id"),
            "title": x.get("videoInfo").get("snippet").get("title"),
            "channelTitle": x.get("videoInfo").get("snippet").get("channelTitle"),
            "thumbnails": x.get("videoInfo").get("snippet").get("thumbnails"),
            "videoId": x.get("videoInfo").get("id"),
            "statistics": x.get("videoInfo").get("statistics"),
            "tags": x.get("videoInfo").get("snippet").get("tags")
        }
        res.append(temp)
    return res

def recommend_videos_mongodb(videos):
    unique_video_ids = set()
    distinct_videos = []

    # Sort videos by likes and view counts
    sorted_videos = sorted(videos, key=lambda x: (int(x['statistics']['likeCount']), int(x['statistics']['viewCount'])), reverse=True)

    # Select the top 10 distinct videos
    for video in sorted_videos:
        if video['videoId'] not in unique_video_ids:
            distinct_videos.append(video)
            unique_video_ids.add(video['videoId'])

        if len(distinct_videos) == 10:
            break

    return distinct_videos

class Neo4jConnection:

    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def search_neo4j(self, labels=None, property=None, order_by=None, limit=None):
        if labels is None and property is None:
            query = "MATCH (n) RETURN n"
        else:
            query = self._build_query(labels, property)

        if order_by is not None:
            query += f" ORDER BY {order_by} DESC"

        if limit is not None:
            query += f" LIMIT {limit}"

        nodes_final = None
        with self._driver.session() as session:
            nodes = session.run(query)
            nodes_final = list(nodes)

        result = []
        for i in nodes_final:
            temp = {}
            for j in i:
                for k in j:
                    temp[k] = j[k]
            result.append(temp)
        return result

    def _build_query(self, labels, property):
        if labels is None:
            labels = ''

        if property is None:
            property = ''

        if type(labels) == str:
            labels = [labels]

        labels = ':'.join(labels)

        properties = ''
        for i in property:
            if 'id' in i or 'Id' in i:
                properties += f"{i}: '{property[i]}',"
            else:
                properties += f"{i}: '{property[i].lower()}',"
        properties = properties[:-1]
        properties = '{' + properties + '}'

        return f"MATCH (n:{labels} {properties}) RETURN n"

def recommend_videos_neo4j(videos, order_by):
    sorted_videos = sorted(videos, key=lambda x: int(x['statistics'][order_by]), reverse=True)
    return sorted_videos[:10]

def combine_recommendations(search_query):
    videos_from_mongodb = search_mongodb(search_query)
    recommended_videos_mongodb = recommend_videos_mongodb(videos_from_mongodb)

    if len(recommended_videos_mongodb) < 10:
        neo4j_site = Neo4jConnection("bolt://localhost:7687", "neo4j", "Renu@8752")
        neo4j_site.connect()

        additional_videos_by_views = neo4j_site.search_neo4j(labels="Video", order_by="n.statistics.viewCount", limit=(10 - len(recommended_videos_mongodb)))

        neo4j_site.close()
        final_recommendations = recommended_videos_mongodb + additional_videos_by_views
    return final_recommendations[:10] 

# Example usage
search_query = "Bangali"
final_recommendations_combined = combine_recommendations(search_query)
print(final_recommendations_combined)
