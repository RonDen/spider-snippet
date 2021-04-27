const mongoose = require('mongoose')
const Schema = mongoose.Schema

var PositionSchema = new Schema({
    account: { type: String, required: true },
    stock: { type: String, required: true },
    quantity: { type: "Number", required: true },
    price: { type: "Number", required: true }
})

module.exports = mongoose.model('Position', PositionSchema)
