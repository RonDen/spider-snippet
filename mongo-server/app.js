const express = require('express')
const bodyParser = require('body-parser')
const position = require('./routes/position')

const app = express()

// MongoDB
const mongoose = require('mongoose')
// mongodb://<user>:<pwd>@<host>:<port>/<database>
uri = 'mongodb://localhost:27017/demo'
mongoose.connect(uri, { useNewUrlParser: true })
const db = mongoose.connection
db.on('error', console.error.bind(console, 'MongoDB connection error'))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded( {extended: false} ))

app.use('/position', position)

const port = 8888
app.listen(port, () => {
    console.log('Position Server is running')
})






