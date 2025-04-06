using Domain;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
using System.Threading.Channels;
using System.Xml.Linq;


namespace App1
{
    public class AddNewClientCustomer
    {
        
        private readonly IChannel _channel;
        private readonly ILogger _logger;

        public AddNewClientCustomer(IChannel channel, ILogger logger)
        {
            _channel = channel;
            _logger = logger;
        }

        async public void StartConsuming()
        {
            string qName = typeof(AddNewClientEvent).Name;
            await _channel.QueueDeclareAsync(queue: qName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new AsyncEventingBasicConsumer(_channel);
            consumer.ReceivedAsync += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                LogInfo($"Recived new message from {qName}': {message}");
                return Task.CompletedTask;
            };

            await _channel.BasicConsumeAsync(queue: qName, autoAck: true, consumer: consumer);
            
            LogInfo("Started listening...");
        }
        public void Run()
        {
            StartConsuming();
            
            LogInfo("Started listening...");
            Console.ReadLine();


        }

        private void LogInfo(string data, [CallerMemberName] string methodName = "")
        {
            _logger.LogInformation("[{Method}] {Message}", methodName, data);
        }
    }
}
