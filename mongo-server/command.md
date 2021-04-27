we can also use db.auth after mongo
db.auth( "userName", "password" )

authentication
right == where + can do what

角色
角色 = 一组权限的集合
read - 读取当前数据库中所有非系统集合
readWrite - 读写当前数据库中的所有非系统集合
dbAdmin - 管理当前数据库
userAdmin - 管理当前数据库中的角色和用户
read/readWrite/dbAdmin/userAdminAnyDatabase - 对所有数据库执行操作，只在admin数据库中提供

// 创建一个只能读取test数据库的用户
```js
use test
db.createUser({
  user: "testReader",
  pwd: "passwd",
  roles: [{role: "read", db: "test"}]
})
```

创建权限
创建一个只能读取accounts集合的用户
roles数组表示希望从哪个角色上继承权限
```js
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
```
mongoexport
导出json或者csv格式文件，要求对所要求导出的数据集具有read权限
```js
use admin
db.createUser({
    user: "readUser",
    pwd: "passwd",
    roles: [ "readAnyDatabase" ]
})
```

将数据库信息导出为cvs文件
```shell
mongoexport --db test --collection accounts --type=csv --fields name, balance --out /opt/backups/accounts.csv -u readUser -p passwd --authenticationDatabase admin
mongoexport --db runoob --collection runoob --type=csv --fields name, balance 
```

也可以使用`.`操作符，导出内嵌文档中的字段

测试导出json文件

更新用户
```js
use poemkg
db.updateUser(
    "poemkg", {
        roles: [{role: "readWrite", db: "poemkg"}]
    }
)
```

导入诗歌数据到MongoDB中

```shell
mongoimport --db poemkg --collection poem --type=json --file /home/luod/PycharmProjects/pythonProject1/ningyangtv/poem-dynasty-1.json -u poemkg -p poemkg --authenticationDatabase admin
mongoimport --db poemkg --collection poem --type=json --file /home/luod/PycharmProjects/pythonProject1/ningyangtv/poem-dynasty-2.json -u poemkg -p poemkg --authenticationDatabase admin
```

导入作者数据到MongoDB中
```shell
mongoimport --db poemkg --collection author --type=json --file /home/luod/PycharmProjects/pythonProject1/results/author-2021-04-22-12_50_23.txt -u poemkg -p poemkg --authenticationDatabase admin
mongoimport --db poemkg --collection author --type=json --file /home/luod/PycharmProjects/pythonProject1/results/author-2021-04-22-12_57_23.txt -u poemkg -p poemkg --authenticationDatabase admin
mongoimport --db poemkg --collection author --type=json --file /home/luod/PycharmProjects/pythonProject1/results/author-2021-04-22-13_00_59.txt -u poemkg -p poemkg --authenticationDatabase admin
```
`mongoimport`可以添加的参数
`--drop`在导入前drop掉之前的collection，确保导入的是新的
`--upsertField`在导入时对指定字段进行校验，如果已经重复，则只做更新而不插入
`--stopOnError`，一旦发现错误立刻停止，确保导入数据质量
`--maintainInsertionOrder`，让mongodb采用json或csv文件中的顺序导入

## mongodb监控工具
`mongostat`和`mongomonior`
确保使用的用户具有`monitor`权限
```shell
use admin
db.createUser({
  user: "monitorUser",
  pwd: "passwd",
  roles: ["clusterMonitor"]
})
```
使用`mongostat`
```shell
mongostat --host localhost --port 27017 -u monitorUser -p passwd --authenticationDatabase admin
```
默认一秒一次的频率，可以在最后指定频率
```shell
# 设置为3秒一次
mongostat --host localhost --port 27017 -u monitorUser -p passwd --authenticationDatabase admin 3
# 只显示5行
mongostat --host localhost --port 27017 -u monitorUser -p passwd --authenticationDatabase admin --rowcount 5
# 只显示想要显示的列
mongostat --host localhost --port 27017 -u monitorUser -p passwd --authenticationDatabase admin -o "command,dirty,used,vsize,res,conn,time"
```
command - 每秒执行的命令数量
dirty, used - 数据库引擎缓存使用比
vsize - 虚拟内存使用量（MB）
res - 常驻内存使用量（MB）
conn - 目前服务器open connection的数量

`mongotop` 显示每个collections上的读写时间

## 常见故障的诊断

MongoDB最常见的故障是响应时间增长
对于一般的web服务而言，响应时间应该在200ms以内
对于一般的mongodb的请求，响应时间应该要在100ms以内

措施：
使用合适的索引，使用explain解释查询

工作集大小超出了RAM的大小
可以在`mongo.conf`文件中添加对内存的大小的使用



```shell

```


