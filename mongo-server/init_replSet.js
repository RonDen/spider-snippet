rs.initiate({
    _id: "mySet",
    members: [
        {_id: 0, host: "mongo1:27017"},
        {_id: 1, host: "mongo2:27018"},
        {_id: 2, host: "mongo3:27019"}
    ]
})

// view the status of the repl set
rs.status()


// mongodb create user, make it admin
// the default user is root
use admin;
db.createUser({
    user: "myAdminUser",
    pwd: "passwd",
    roles: [ "userAdminAnyDatabase" ]
})

// step2.
// conection the the mongodb servce
// mongo -u "myAdminUser" -p "passwd" --authenticationDatabase "admin"

show dbs

use admin
use poemkg

show collections

use admin
db.auth("myAdminUser", "passwd")


{ resource: {db: "test", collection: ""}, actions: ["find", "update"] }
{ resource: {cluster: true}, actions: ["shutdown"] }
