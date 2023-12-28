from typing import Any
import os
import pandas as pd
import pymongo
import json
from ensure import ensure_annotations


class mongo_operation:
    """
    A single call to MongoDB operation.
    
    -------
    PARAMS:
        client_url: The client url that you get from mongodb webpage.
        database_name: The database one wants to connect to.
        collection_name: The name of the collection you want to connect to.
        
    """
    __collection = None # a variable that will be storing the collection name
    __database = None # a variable that will be storing the database name
    
    def __init__(self, client_url: str, database_name: str,collection_name:str =  None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
        
    @property
    def __create_mongo_client(self):
        """to create a MongoClient instance

        Returns:
            client: mongodb client instance
        """
        client = pymongo.MongoClient(self.client_url)
        return client
    
    @property        
    def __connect_database(self):
        """for connenting the database

        Returns:
            database: database object of mongodb
        """
        if mongo_operation.__database == None:
            self.database = self.__create_mongo_client[self.database_name]
        return self.database
    
    
    @ensure_annotations
    def set_new_database(self, database:str):
        """to set a new database name for the MongoClient

        Args:
            database : pass the new database name that is going to be used for the next operations.
        """
        self.database = self.__create_mongo_client[database]
        mongo_operation.__database = database
        self.database_name = database

    @property
    def __connect_collection(self):
        """for connenting the collection instance

        Returns:
            collection : collection instance of mongodb
        """
        if mongo_operation.__collection == None:
            self.collection = self.__connect_database[self.collection_name]
        
        return self.collection
    
    @ensure_annotations
    def set_new_collection(self,collection_name:str):
        """ to set a new collection name for mongo_operation

        Args:
            collection_name (str): pass new collection name that is going to be used for the next operations.
        """
        self.collection = self.__connect_database[collection_name]
        mongo_operation.__collection = collection_name
        self.collection_name = collection_name
    @ensure_annotations
    def insert_record(self, record: dict, collection_name:str) -> Any: 
        """
        insert one record to mongodb

        ------
        :params
           
            record: dict,
                    the data to insert into mongodb. 
            
                    
        example: 
                #for one record
                insert_record( record = {'name':'python'})

                #for multiple record
                insert_record(
                            record = [
                                        {'name':'python',
                                        'used_as': 'programming_language'},
                                        {'name': 'R',
                                        'used_as': 'programming_language'}
                                        ]
                            )
        """

        self.set_new_collection(collection_name =  collection_name)
        if type(record) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError('record must be a dictionary. Example is given in the docstring of this function.')
            self.__connect_collection.insert_many(record)
        elif type(record)== dict:
            self.__connect_collection.insert_one(record)


    @ensure_annotations
    def bulk_insert(self, dataframe ,collection_name:str = None, **kwargs ):
        """ insert data from dataframe object / csv /excel file to mongodb
        
        ------
        PARAMS: 
              dataframe : path of the csv file or pandas dataframe object
              
              **kwargs :
                        any parameters of pandas read function.
        
        """

        if collection_name:
           self.set_new_collection = collection_name

        if not isinstance(dataframe, pd.DataFrame):
            
            path = dataframe
            if path.endswith('.csv'):
                dataframe = pd.read_csv(path, encoding='utf8', **kwargs)
            elif path.endswith('.xlsx'):
                dataframe = pd.read_excel(path, encoding = 'utf8', **kwargs)

    
            
        data_json = json.loads(dataframe.to_json(orient='records'))
        self.__connect_collection.insert_many(data_json)
       

    @ensure_annotations
    def find(self, collection_name:str = None,  query:dict={}) :
        """
        To find data in mongo database
        returns dataframe of the searched data. 
        
        PARAMS: 
              query: dict, default : {} which will be fetching all data from the collection
                    query to find the data in mongo database 
                    -- example of query -- {"name":"sourav"}
        """
        if collection_name:
           self.set_new_collection = collection_name
            
        if self.collection_name not in self.__connect_database.list_collection_names():
            raise NameError("""Collection not found in mongo database. Following could be the reason.
                              1. Check the spelling or check the name of the collection.
                              2. It might be possible that the collection is empty and does not contain any data. Try to insert some data and then try to find the data.
                              3. The collection is yet not created. 
                              4. If you have changed the name of the collection or database, check whether it contains some data or not.
                                    """)
        
        

        cursor = self.__connect_collection.find(query)
        data =  pd.DataFrame(list(cursor))
    

        return data


    @ensure_annotations
    def update(self, where_condition:dict,update_query:dict, update_all_data = False):
        """
        To update data in mongo database
        
        PARAMS:
                where_condition: dict,
                               to find the data in mongo database -- example of query {"name":"sourav"}
                update_query : dict,
                               query to update the data in mongo database -- example of query -- {"name":"Rahul"}"
                update_all : Bool,
                                if True, update all data in mongo database 
        EXAMPLE:
                
                where_condition = {"name":'Rahul Roy'}
                update_query = {"name":'Sourav Roy'}

                ## it'll updata name from Rahul Roy to Sourav Roy.

        """



        if update_all_data:
            self.__connect_collection.update_many(where_condition, {'$set':update_query})
        else:
            self.__connect_collection.update_one(where_condition, {'$set':update_query})
        

    @ensure_annotations
    def delete_record(self, where_condition:dict, delete_all=False):
        """_summary_

        Args:
            where_condition (dict): 
                                column name and value upon which the delete
                                operation will be performed should be passed
                                as dictionary.
                                example:
                                        {'name':'Rahul Roy'} -- here column name is name and value is Rahul Roy.
            delete_all (bool, optional): 
                            If multiple records are to be deleted, value would be True. 
                            Default- False.
        """
        if delete_all:
            self.__connect_collection.delete_many(where_condition)
        else:
            self.__connect_collection.delete_one(where_condition)
