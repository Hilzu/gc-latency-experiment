package main

const windowSize int = 200000
const msgCount int = 1000000
const msgSize int = 1024
var m map[int][msgSize]byte = make(map[int][msgSize]byte)

func fill(bs [msgSize]byte, b byte) {
  for i, _ := range bs {
    bs[i] = b
  }
}

func createMessage(n int) [msgSize]byte {
  var msg [msgSize]byte
  fill(msg, byte(n))
  return msg
}

func pushMessage(m map[int][msgSize]byte, id int) {
  var lowId int = windowSize - id
  m[id] = createMessage(id)
  if (lowId >= 0) {
    delete(m, lowId)
  }
}

func main() {
  for i := 0; i < msgCount; i++ {
    pushMessage(m, i)
  }
}
