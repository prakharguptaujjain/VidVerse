import os
import json
from neo4j import GraphDatabase
import time

class Neo4jConnection:
    def __init__(self, uri, user, password):
        """
        uri: bolt://localhost:7687
        user: neo4j
        password: 1234567890
        """
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        """
        Close the connection
        """
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        """
        Connect to the database
        """
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def relations(self, labels = None, property = None, query = None):
        """
        Get relations from database of a node
        """

        if query != None:
            nodes_final = None
            with self._driver.session() as session:
                nodes = session.run(query)
                nodes_final = list(nodes)
            return nodes_final
        
        if labels == None and property == None and query == None:
            query = "MATCH (n)-[r]->(m) RETURN n, r, m"
            nodes_final = None
            with self._driver.session() as session:
                nodes = session.run(query)
                nodes_final = list(nodes)
            return nodes_final
        
        if labels == None:
            labels = ''

        if property == None:
            property = ''

        if type(labels) == str:
            labels = [labels]

        labels = ':'.join(labels)

        properties = ''
        for i in property:
            properties += f"{i}: '{property[i].lower()}',"
        properties = properties[:-1]
        properties = '{' + properties + '}'

        query = f"MATCH (n:{labels} {properties})-[r]->(m) RETURN n, r, m"

    def search(self, labels = None, property = None, query = None):
        """
        Search in database
        """
        if query != None:
            nodes_final = None
            with self._driver.session() as session:
                nodes = session.run(query)
                nodes_final = list(nodes)
            return nodes_final
        
        if labels == None and property == None and query == None:
            query = "MATCH (n) RETURN n"
            nodes_final = None
            with self._driver.session() as session:
                nodes = session.run(query)
                nodes_final = list(nodes)
            return nodes_final
        
        if labels == None:
            labels = ''

        if property == None:
            property = ''

        if type(labels) == str:
            labels = [labels]

        labels = ':'.join(labels)

        properties = ''
        for i in property:
            properties += f"{i}: '{property[i].lower()}',"
        properties = properties[:-1]
        properties = '{' + properties + '}'

        query = f"MATCH (n:{labels} {properties}) RETURN n"
        nodes_final = None
        with self._driver.session() as session:
            nodes = session.run(query)
            nodes_final = list(nodes)
        return nodes_final
    
    def exist(self, labels, property):
        """
        Check if the node exist in database
        """
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
            properties += f"{i}: '{property[i].lower()}',"
        
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
        """
        Insert node in database
        """
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
            properties += f"{i}: '{property[i].lower()}',"
        properties = properties[:-1]
        properties = '{' + properties + '}'

        query = f"CREATE (n:{labels} {properties})"

        with self._driver.session() as session:
            session.run(query)

    def delete(self, labels = None, property = None):
        """
        Delete node in database
        """
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
            properties += f"{i}: '{property[i].lower()}',"

        if properties != '':
            properties = properties[:-1]
            properties = '{' + properties + '}'

        query = f"MATCH (n:{labels} {properties}) DETACH DELETE n"
        with self._driver.session() as session:
            session.run(query)

    def relation(self, label1, property1, label2, property2, relation):
        """
        Create relation between two nodes
        """
        if type(label1) == str:
            label1 = [label1]
        
        if type(label2) == str:
            label2 = [label2]
        
        label1 = ':'.join(label1)
        label2 = ':'.join(label2)

        properties1 = ''
        for i in property1:
            properties1 += f"{i}: '{property1[i].lower()}',"
        properties1 = properties1[:-1]
        properties1 = '{' + properties1 + '}'

        properties2 = ''
        for i in property2:
            properties2 += f"{i}: '{property2[i].lower()}',"
        properties2 = properties2[:-1]
        properties2 = '{' + properties2 + '}'

        query = f"MATCH (n:{label1} {properties1}), (m:{label2} {properties2}) CREATE (n)-[:{relation}]->(m)"
        with self._driver.session() as session:
            session.run(query)

# site = Neo4jConnection("bolt://localhost:7687", "neo4j", "1234567890")

# site.connect()
# site.close()