"""
This file stores the data from the json files into the Neo4j database.
Enter correct path of the dataset folder in line 184.
"""

import os
import json
from neo4j import GraphDatabase
import time

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

    def search(self, query):
        nodes_final = None
        with self._driver.session() as session:
            nodes = session.run(query)
            nodes_final = list(nodes)
        return nodes_final
    
    def exist(self, labels, property):
        if labels == None or property == None:
            return False
        
        if labels == None:
            labels = ''

        if property == None:
            property = ''

        if type(labels) == str:
            labels = [labels]

        labels = ':'.join(labels)

        properties = ''
        for i in property:
            properties += f"{i}: '{property[i]}',"
        
        if properties != '':
            properties = properties[:-1]
            properties = '{' + properties + '}'

        query = f"MATCH (n:{labels} {properties}) RETURN n"
        with self._driver.session() as session:
            nodes = session.run(query)
            nodes_final = list(nodes)

        if len(nodes_final) == 0:
            return False
        return True

    def insert(self, labels = None, property = None, query = None):
        if query != None:
            with self._driver.session() as session:
                session.run(query)
            return
        if labels == None or property == None:
            return
        
        if self.exist(labels, property):
            return

        if type(labels) == str:
            labels = [labels]

        labels = ':'.join(labels)

        properties = ''
        for i in property:
            properties += f"{i}: '{property[i]}',"
        properties = properties[:-1]
        properties = '{' + properties + '}'

        query = f"CREATE (n:{labels} {properties})"

        with self._driver.session() as session:
            session.run(query)

    def delete(self, labels = None, property = None):
        if labels == None and property == None:
            query = "MATCH (n) DETACH DELETE n"
            with self._driver.session() as session:
                session.run(query)
            return
        
        if labels == None:
            labels = ''

        if property == None:
            property = ''

        if type(labels) == str:
            labels = [labels]
        
        labels = ':'.join(labels)

        properties = ''
        for i in property:
            properties += f"{i}: '{property[i]}',"

        if properties != '':
            properties = properties[:-1]
            properties = '{' + properties + '}'

        query = f"MATCH (n:{labels} {properties}) DETACH DELETE n"
        with self._driver.session() as session:
            session.run(query)

    def relation(self, label1, property1, label2, property2, relation):
        if type(label1) == str:
            label1 = [label1]
        
        if type(label2) == str:
            label2 = [label2]
        
        label1 = ':'.join(label1)
        label2 = ':'.join(label2)

        properties1 = ''
        for i in property1:
            properties1 += f"{i}: '{property1[i]}',"
        properties1 = properties1[:-1]
        properties1 = '{' + properties1 + '}'

        properties2 = ''
        for i in property2:
            properties2 += f"{i}: '{property2[i]}',"
        properties2 = properties2[:-1]
        properties2 = '{' + properties2 + '}'

        query = f"MATCH (n:{label1} {properties1}), (m:{label2} {properties2}) CREATE (n)-[:{relation}]->(m)"
        with self._driver.session() as session:
            session.run(query)

    def update(self, query):
        with self._driver.session() as session:
            session.run(query)

    def insert_and_relate(self, label1, property1, label2, property2, relation):
        if self.exist(label1, property1):
            return
        
        if type(label1) == str:
            label1 = [label1]

        if type(label2) == str:
            label2 = [label2]

        label1 = ':'.join(label1)
        label2 = ':'.join(label2)

        properties1 = ''
        for i in property1:
            properties1 += f"{i}: '{property1[i]}',"
        properties1 = properties1[:-1]
        properties1 = '{' + properties1 + '}'

        properties2 = ''
        for i in property2:
            properties2 += f"{i}: '{property2[i]}',"
        properties2 = properties2[:-1]
        properties2 = '{' + properties2 + '}'


    
site = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", password="1234567890")

site.connect()

site.delete()

path = 'D:\Adarsh\C++\DE\Project\VidVerse\dataset\\test\\'
files = os.listdir(path)

x = 0
query = []
count = 1
tag_map = {}

val = 0
for file in files:
    x += 1
    path1 = path + file
    data = json.load(open(path1))['videoInfo']
    properties = {
        'id': data['id'],
        'title': data['snippet']['title'].replace('"', "'"),
        'channelTitle': data['snippet']['channelTitle'].replace('"', "'"),
        'channelId': data['snippet']['channelId'].replace('"', "'"),
    }

    prop = ''
    for i in properties:
        prop += f'{i}: "{properties[i]}",'
    prop = prop[:-1]
    prop = '{' + prop + '}'
    video = f"video{count}"
    count += 1
    query.append(f"({video}:Video {prop})")

    if 'tags' not in data['snippet']:
        continue

    tags = data['snippet']['tags']

    for tag in tags:
        properties = {
            'name': tag.lower()
        }
        prop = ''
        for i in properties:
            prop += f'{i}: "{properties[i]}",'
        prop = prop[:-1]
        prop = '{' + prop + '}'

        if tag in tag_map:
            query.append(f"({tag_map[tag]})-[:IsTag]->({video})")
            continue

        tag_map[tag] = f"tag{len(tag_map) + 1}"
        query.append(f"({tag_map[tag]}:Tag {prop})")
        query.append(f"({tag_map[tag]})-[:IsTag]->({video})")
    
    val += 1
    print("Videos done: ", val)

query = 'CREATE ' + ','.join(query)

site.insert(query = query)

site.close()