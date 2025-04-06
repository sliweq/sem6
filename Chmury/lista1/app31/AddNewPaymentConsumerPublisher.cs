using Microsoft.Extensions.Logging;
using RabbitMQ.Client.Events;
using RabbitMQ.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using domain3;
using System.Text.Json;
using System.Runtime.CompilerServices;

namespace app3
{
    class AddNewPaymentConsumerPublisher
    {

        private readonly IChannel _channel;
        private readonly ILogger _logger;

        public AddNewPaymentConsumerPublisher(IChannel channel, ILogger logger)
        {
            _channel = channel;
            _logger = logger;
        }

        public void Publish<T>(T eventMess)
        {
            string qName = eventMess.GetType().Name;
            _channel.QueueDeclareAsync(queue: qName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            string mess = JsonSerializer.Serialize(eventMess);
            var body = Encoding.UTF8.GetBytes(mess);

            _channel.BasicPublishAsync(exchange: string.Empty, routingKey: eventMess.GetType().Name, body: body);
            LogInfo("Published new message");
        }

        public void StartConsuming()
        {
            string qName = typeof(AddNewPaymentEvent).Name;
            _channel.QueueDeclareAsync(queue: qName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new AsyncEventingBasicConsumer(_channel);
            consumer.ReceivedAsync += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                LogInfo($"Recived new message from {qName}': {message}");

                Publish(new PaymentConfirmationEvent()
                {
                    EventId = Guid.NewGuid(),
                    Data = "New Payment Confirmtion"
                });

                return Task.CompletedTask;
            };

            _channel.BasicConsumeAsync(queue: qName, autoAck: true, consumer: consumer);
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
            _logger.LogInformation("[{Method}] {Message}", methodName, data );
        }
    }
}
