"use strict";

const windowSize = 200000
const msgCount = 1000000
const msgSize = 1024

function createMessage (n) {
  return Buffer.alloc(msgSize, n % 256)
}

function pushMessage (map, id) {
  const lowId = id - windowSize
  map.set(id, createMessage(id))
  if (lowId >= 0) {
    map.delete(lowId)
  }
}

const map = new Map()
for (let i = 0; i < msgCount; i++) {
  pushMessage(map, i)
}
