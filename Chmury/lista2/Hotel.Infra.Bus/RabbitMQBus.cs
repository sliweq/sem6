﻿using Hotel.Common.Domain.Bus;
using Hotel.Common.Domain.Commands;
using Hotel.Common.Domain.Events;
using MediatR;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Text;
using static Microsoft.IO.RecyclableMemoryStreamManager;


namespace Hotel.Infra.Bus
{
    public sealed class RabbitMQBus : IEventBus
    {
        private readonly IMediator _mediator;
        private readonly Dictionary<string, List<Type>> _handlers;
        private readonly List<Type> _eventTypes;
        private readonly IServiceScopeFactory _serviceScopeFactory;
        private readonly IConfiguration _configRoot;
        private readonly ILogger<RabbitMQBus> _logger;

        public RabbitMQBus(IMediator mediator, IServiceScopeFactory serviceScopeFactory, IConfiguration configRoot, ILogger<RabbitMQBus> logger)
        {
            _mediator = mediator;
            _handlers = new Dictionary<string, List<Type>>();
            _eventTypes = new List<Type>();
            _serviceScopeFactory = serviceScopeFactory;
            _configRoot = configRoot;
            _logger = logger;
        }

        public Task SendCommand<T>(T command) where T : Command
        {
            _logger.LogInformation($"Rabbit MQ Send Command {command.GetType()}");
            return _mediator.Send(command);
        }

        public async Task Publish<T>(T @event) where T : Event
        {
            _logger.LogInformation($"Rabbit MQ Published Event {@event.GetType().Name}");
            var factory = new ConnectionFactory() {};
            factory.Uri = new Uri(_configRoot["AmqpSettings:Amqpurl"]);

            using (var connection = await factory.CreateConnectionAsync())
            using (var channel = await connection.CreateChannelAsync())
            {
                var eventName = @event.GetType().Name;

                //await channel.QueueDeclareAsync(eventName, false, false, false, null);
                await channel.ExchangeDeclareAsync(eventName, ExchangeType.Fanout);

                var message = JsonConvert.SerializeObject(@event);
                var body = Encoding.UTF8.GetBytes(message);

                //await channel.BasicPublishAsync("", eventName, body);
                await channel.BasicPublishAsync(eventName, "", body);

            }
        }

        public async Task Subscribe<T, TH>()
            where T : Event
            where TH : IEventHandler<T>
        {
            var eventName = typeof(T).Name;
            var handlerType = typeof(TH);

            _logger.LogInformation($"Rabbit MQ Subscribed Event {eventName}");

            if (!_eventTypes.Contains(typeof(T)))
            {
                _eventTypes.Add(typeof(T));
            }

            if (!_handlers.ContainsKey(eventName))
            {
                _handlers.Add(eventName, new List<Type>());
            }

            if (_handlers[eventName].Any(s => s.GetType() == handlerType))
            {
                _logger.LogError($"Handler Type {handlerType.Name} already is registered for {eventName}", nameof(handlerType));
                throw new ArgumentException($"Handler Type {handlerType.Name} already is registered for {eventName}", nameof(handlerType));
            }

            _handlers[eventName].Add(handlerType);

            await StartBasicConsumeAsync<T>();
        }

        private async Task StartBasicConsumeAsync<T>() where T : Event
        {
            var factory = new ConnectionFactory() { };
            factory.Uri = new Uri(_configRoot["AmqpSettings:Amqpurl"]);

            _logger.LogInformation($"Rabbit MQ Started basic consuption Subscribed Event {typeof(T).Name}");

            var connection = await factory.CreateConnectionAsync();
            var channel = await connection.CreateChannelAsync();

            var exchangeName = typeof(T).Name;

            await channel.ExchangeDeclareAsync(exchangeName, ExchangeType.Fanout);

            var queueName = $"{exchangeName}_{Guid.NewGuid()}";
            //var queueName = $"exchangeName";

            await channel.QueueDeclareAsync(queueName, false, false, false, null);
            await channel.QueueBindAsync(queueName, exchangeName, "");

            var consumer = new AsyncEventingBasicConsumer(channel);
            consumer.ReceivedAsync += Consumer_Received;

            await channel.BasicConsumeAsync(queueName, true, consumer);


            //var eventName = typeof(T).Name;

            //await channel.QueueDeclareAsync(eventName, false, false, false, null);

            //var consumer = new AsyncEventingBasicConsumer(channel);

            //consumer.ReceivedAsync += Consumer_Received;

            //await channel.BasicConsumeAsync(eventName, true, consumer);
        }

        private async Task Consumer_Received(object sender, BasicDeliverEventArgs @event)
        {
            //var eventName = @event.RoutingKey;

            _logger.LogInformation($"Rabbit MQ Started basic consuption recieved Event {@event.Exchange}");

            var eventName = @event.Exchange;
            var message = Encoding.UTF8.GetString(@event.Body.ToArray());
            try
            {
                await ProcessEvent(eventName, message).ConfigureAwait(false);
            }
            catch (Exception ex) { }
        }

        private async Task ProcessEvent(string eventName, string message)
        {
            //Console.WriteLine("Recieved some event asdasd");
            //Console.WriteLine(_handlers);
            //Console.WriteLine(_handlers.Keys);
            //Console.WriteLine(eventName);

            if (_handlers.ContainsKey(eventName))
            {
                _logger.LogInformation($"Rabbit MQ Processing Event {eventName}");
                using (var scope = _serviceScopeFactory.CreateScope())
                {
                    var subscriptions = _handlers[eventName];

                    foreach (var subscription in subscriptions)
                    {
                        var handler = scope.ServiceProvider.GetService(subscription);
                        if (handler == null) continue;
                        
                        var eventType = _eventTypes.SingleOrDefault(t => t.Name == eventName);
                        var @event = JsonConvert.DeserializeObject(message, eventType);
                        var concreteType = typeof(IEventHandler<>).MakeGenericType(eventType);

                        await (Task)concreteType.GetMethod("Handle").Invoke(handler, new object[] { @event });
                    }
                }

            }
        }
    }
}
