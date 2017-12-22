import pymongo
import ssl


class Database(object):
    client = pymongo.MongoClient("mongodb+srv://test:mM64*$yX1u@test1-ho0db.mongodb.net/test",
                                 ssl=True,
                                 ssl_cert_reqs=ssl.CERT_NONE
                                 )
