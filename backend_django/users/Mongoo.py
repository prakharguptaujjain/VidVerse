from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_keywords(input_string):
    words = word_tokenize(input_string)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", "'", '"', ",", ".", "/", "<", ">", "?", "|", "`", "~"]
    filtered_words = [word for word in filtered_words if word not in symbols]
    keywords = list(set(filtered_words))
    return keywords

def search(s: str):
    """
    Searches the database for a given string and returns a dictionary of results
    """
    # Connect to the database
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
            "statistics": x.get("videoInfo").get("statistics")
        }
        res.append(temp)
    return res

def like(video):
    """
    Increments the like count of a video
    """

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    document = collection.find_one({"_id": video["_id"]})
    collection.update_one({"_id": video["_id"]}, {"$set": {"videoInfo.statistics.likeCount": int(document.get("videoInfo").get("statistics").get("likeCount")) + 1}})
    return

def dislike(video):
    """
    Increments the dislike count of a video
    """

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    document = collection.find_one({"_id": video["_id"]})
    collection.update_one({"_id": video["_id"]}, {"$set": {"videoInfo.statistics.dislikeCount": int(document.get("videoInfo").get("statistics").get("dislikeCount")) + 1}})
    return

def unlike(video):
    """
    Decrements the like count of a video
    """

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    document = collection.find_one({"_id": video["_id"]})
    collection.update_one({"_id": video["_id"]}, {"$set": {"videoInfo.statistics.likeCount": int(document.get("videoInfo").get("statistics").get("likeCount")) - 1}})
    return

def undislike(video):
    """
    Decrements the dislike count of a video
    """

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    document = collection.find_one({"_id": video["_id"]})
    collection.update_one({"_id": video["_id"]}, {"$set": {"videoInfo.statistics.dislikeCount": int(document.get("videoInfo").get("statistics").get("dislikeCount")) - 1}})
    return

def get_video(videoId):
    """
    Get videos from the database for a given videoId and returns a list of results
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["VidVerse"]
    collection = db["videos"]

    query = {
        "videoInfo.id": videoId
    }
    projection = {
        "_id": 1,
        "videoInfo.snippet.title": 1,
        "videoInfo.snippet.channelTitle": 1,
        "videoInfo.snippet.thumbnails": 1,
        "videoInfo.id": 1,
        "videoInfo.statistics": 1
    }

    results = collection.find(query, projection)
    res = []
    for x in results:
        temp = {
            "_id": x.get("_id"),
            "title": x.get("videoInfo").get("snippet").get("title"),
            "channelTitle": x.get("videoInfo").get("snippet").get("channelTitle"),
            "thumbnails": x.get("videoInfo").get("snippet").get("thumbnails"),
            "videoId": x.get("videoInfo").get("id"),
            "statistics": x.get("videoInfo").get("statistics")
        }
        res.append(temp)
    return res

# print(get_video("-0ziqk9cZRM"))
