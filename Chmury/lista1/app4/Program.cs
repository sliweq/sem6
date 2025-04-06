﻿using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;

namespace app4
{
    public class RunReceiver
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

            ILogger logger = logFactory.CreateLogger("app4");
            logger.LogInformation("Starting consumer app4");

            var factory = new ConnectionFactory() { };
            factory.Uri = new Uri(root["AmqpSettings:Amqpurl"]);
            using (var connection = await factory.CreateConnectionAsync())
            {
                using (var channel = await connection.CreateChannelAsync())
                {

                    AddNewPaymentConfirmationConsumer bibliotekaPublisher = new AddNewPaymentConfirmationConsumer(channel, logger);
                    bibliotekaPublisher.Run();
                }
            }
        }
    }
}
