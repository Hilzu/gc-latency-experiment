let windowSize = 200_000
let msgCount = 10_000_000
let msgSize = 1024

func createMessage(_ n: Int) -> Array<UInt8> {
    return Array<UInt8>(repeating: UInt8(n % 256), count: msgSize)
}

func pushMessage (map: inout [Int: Array<UInt8>], id: Int) {
    let lowId = id - windowSize
    map[id] = createMessage(id)
    if lowId >= 0 {
        map.removeValue(forKey: lowId)
    }
}

var map = [Int: Array<UInt8>]()
for i in 0...(msgCount - 1) {
    pushMessage(map: &map, id: i)
}
