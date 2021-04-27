# create a network
docker network create mongonetwork

# show all network
docker network ls

# run three mongod node
docker run --net mongonetwork --name mongo1 -v ~/mymongo/data1:/data/db -p 27017:27017 -d mongo:4 --replSet myset --port 27017

docker run --net mongonetwork --name mongo2 -v ~/mymongo/data1:/data/db -p 27018:27018 -d mongo:4 --replSet myset --port 27018

docker run --net mongonetwork --name mongo3 -v ~/mymongo/data1:/data/db -p 27019:27019 -d mongo:4 --replSet myset --port 27019

# init the replSet by hand
docker exec -it mongo1 mongo

docker run --name mymongo -v /mymongo/data:/data/db -d mongo:4
docker run --name mymongo -v /mymongo/data:/data/db -d mongo:4 mongod

docker stop mymongo && docker rm $_

docker run --name mymongo -v /mymongo/data:/data/db -d mongo:4 mongod --auth

# connect to the mongod with authentication
# must specify the authenticationDatabase
mongo -u "myAdminUser" -p "passwd" --authenticationDatabase "admin"

# we can also use db.auth after mongo
# db.auth( "userName", "password" )

# authentication
# right == where + can do what

角色
角色 = 一组权限的集合
read - 读取当前数据库中所有非系统集合
readWrite - 读写当前数据库中的所有非系统集合
dbAdmin - 管理当前数据库
userAdmin - 管理当前数据库中的角色和用户
read/readWrite/dbAdmin/userAdminAnyDatabase - 对所有数据库执行操作，只在admin数据库中提供

// 创建一个只能读取test数据库的用户
use test
db.createUser({
  user: "testReader",
  pwd: "passwd",
  roles: [{role: "read", db: "test"}]
})

创建权限
创建一个只能读取accounts集合的用户
# roles数组表示希望从哪个角色上继承权限
use test
db.createRole({
  role: "readAccounts",
  privileges: [{resource: {db: "test", collection: "accounts"}, actions: ["find"]}],
  roles: []
})

use test
db.createUser({
  user: "accountsReader",
  pwd: "passwd",
  roles: ["readAccounts"]
})

mongoexport
导出json或者csv格式文件，要求对所要求导出的数据集具有read权限





