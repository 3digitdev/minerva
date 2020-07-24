// https://docs.mongodb.com/manual/tutorial/write-scripts-for-the-mongo-shell/

conn = new Mongo("localhost:27017");
db = conn.getDB("minerva");

colls = [
	"api_keys",
    "dates",
    "employments",
    "housings",
    "links",
    "logins",
    "access_logs",
    "notes",
    "recipes",
    "tags",
];

for(var i = 0; i < colls.length; i++) {
	collName = colls[i];
	db.createCollection(collName);
}

db['tags'].createIndex({"name": 1}, {unique: true});
db['access_logs'].createIndex({created_at: 1}, {expireAfterSeconds: 604800});