using Microsoft.Extensions.Logging;
using RabbitMQ.Client;
using System.Collections.Generic;
using domain7; 
using System.Text;
using System.Text.Json;
using System.Runtime.CompilerServices;

namespace app7
{
    public class AddNewPaymentPublisher
    {
        private readonly IChannel _channel;
        private readonly ILogger _logger;
        public AddNewPaymentPublisher(IChannel ichannel, ILogger logger)
        {
            _channel = ichannel;
            _logger = logger;
        }

        async public void Publish<T>(T eventMess)
        {
            string qName = eventMess.GetType().Name;
            await _channel.QueueDeclareAsync(queue: qName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            string mess = JsonSerializer.Serialize(eventMess);
            var body = Encoding.UTF8.GetBytes(mess);

            await _channel.BasicPublishAsync(exchange: string.Empty, routingKey: eventMess.GetType().Name, body: body);
            LogInfo("Added new message");
        }


        public void Run()
        {
            while (true)
            {
                Publish(
                    new AddNewPaymentEvent()
                    {
                        EventId = Guid.NewGuid(),
                        Data = "New Client"
                    }
                    );

                
                Thread.Sleep(5000);

            }
        }

        private void LogInfo(string data, [CallerMemberName] string methodName = "")
        {
            _logger.LogInformation("[{Method}] {Message}", methodName, data);
        }

    }
}
