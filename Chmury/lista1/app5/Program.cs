using RabbitMQ.Client;
using System.Net;
using System.Text;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using System;
using System.IO;

namespace app5
{
    public class RunPublisher
    {

        public static async void Main(string[] args)
        {
            IConfigurationBuilder builder = new ConfigurationBuilder().SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), "..")).AddJsonFile("appsettings.json", false, true);
            IConfigurationRoot root = builder.Build();

            using ILoggerFactory logFactory = LoggerFactory.Create(builder => builder
            .AddSimpleConsole(options =>
            {
                options.SingleLine = true;
                options.TimestampFormat = "HH:mm:ss ";
            })
            .SetMinimumLevel(LogLevel.Information));

            ILogger logger = logFactory.CreateLogger("app5");
            logger.LogInformation("Starting publisher app5 - Main");

            var factory = new ConnectionFactory(){};
        
            factory.Uri = new Uri(root["AmqpSettings:Amqpurl"]);

            using (var connection = await factory.CreateConnectionAsync())
            {
                using (var channel = await connection.CreateChannelAsync())
                {
                    AddNewClientPublisher sender = new AddNewClientPublisher(channel, logger);
                    sender.Run();

                }
            }
        }
    }
}
