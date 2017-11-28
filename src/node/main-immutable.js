"use strict"

const Immutable = require("immutable")

const windowSize = 200000
const msgCount = 1000000
const msgSize = 1024

const createMessage = n => Buffer.alloc(msgSize, n % 256)

const pushMessage = (map, id) => {
  const lowId = id - windowSize
  const inserted = map.set(id, createMessage(id))
  return lowId >= 0 ? inserted.delete(lowId) : inserted
}

const map = new Immutable.Map()

new Immutable.Range(0, msgCount).reduce((map, i) => pushMessage(map, i), map)
