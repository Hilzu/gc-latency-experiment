object Main {
  val windowSize = 200000
  val msgCount = 1000000
  val msgSize = 1024

  def createMessage(n: Int): Array[Byte] = {
    Array.fill(msgSize){ n.toByte }
  }

  def pushMessage(map: Map[Int, Array[Byte]], id: Int): Map[Int, Array[Byte]] = {
    val lowId = id - windowSize
    val inserted = map + (id -> createMessage(id))
    if (lowId >= 0) inserted - lowId else inserted
  }

  def main(args: Array[String]): Unit = {
    val map = Map[Int, Array[Byte]]()
    (0 until msgCount).foldLeft(map) { (m, i) => pushMessage(m, i) }
  }
}
