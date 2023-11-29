import org.apache.spark.sql.SparkSession
import org.testcontainers.containers.Neo4jContainer
import org.neo4j.spark._

object Main extends App {
    // Start a Neo4j test container
    val neo4jContainer = new Neo4jContainer("neo4j:latest")
    neo4jContainer.start()

    // Setup Spark session
    val spark = SparkSession.builder()
      .appName("App")
      .master("local[*]")
      .getOrCreate()

    // Configure Neo4j Spark connector
    val neo4jOptions = Map(
      "url" -> s"bolt://localhost:${neo4jContainer.getMappedPort(7687)}",
      "authentication.basic.username" -> "neo4j",
      "authentication.basic.password" -> neo4jContainer.getAdminPassword
    )

    // Example query using the connector
    val df = spark.read.format("org.neo4j.spark.DataSource")
      .options(neo4jOptions)
      .option("labels", "YourLabel")
      .load()

    // Do something with the DataFrame
    df.show()

    // Stop the container after the test
    neo4jContainer.stop()

    // Stop Spark session
    spark.stop()
}
