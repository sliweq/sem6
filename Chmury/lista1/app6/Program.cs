using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;

namespace app6
{
    public class RunPublisher
    {

        public static async void Main(string[] args)
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), ".."))
                .AddJsonFile("appsettings.json", false, true);
            IConfigurationRoot root = builder.Build();

            using ILoggerFactory logFactory = LoggerFactory.Create(builder => builder
            .AddSimpleConsole(options =>
            {
                options.SingleLine = true;
                options.TimestampFormat = "HH:mm:ss ";
            })
            .SetMinimumLevel(LogLevel.Information));

            ILogger logger = logFactory.CreateLogger("app6");
            logger.LogInformation("Starting app6");

            var factory = new ConnectionFactory() { };

            factory.Uri = new Uri(root["AmqpSettings:Amqpurl"]);

            using (var connection = await factory.CreateConnectionAsync())
            {
                using (var channel = await connection.CreateChannelAsync())
                {
                    AddNewReservationPublisher sender = new AddNewReservationPublisher(channel, logger);
                    sender.Run();

                }
            }
        }
    }
}
