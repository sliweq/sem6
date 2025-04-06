using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App1
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

            ILogger logger = logFactory.CreateLogger("app1");
            logger.LogInformation("Starting app1");

            var factory = new ConnectionFactory(){};
            factory.Uri = new Uri(root["AmqpSettings:Amqpurl"]);
            using (var connection = await factory.CreateConnectionAsync())
            {
                using (var channel = await connection.CreateChannelAsync())
                {

                    AddNewClientCustomer bibliotekaPublisher = new AddNewClientCustomer(channel, logger);
                    bibliotekaPublisher.Run();
                }
            }
        }
    }
}
