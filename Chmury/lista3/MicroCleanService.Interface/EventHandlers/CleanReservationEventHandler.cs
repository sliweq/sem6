using Hotel.Common.Domain.Bus;
using MediatR;
using MicroCleanService.Domain.Commands;
using MicroCleanService.Domain.Events;
using Microsoft.Extensions.Logging;


namespace MicroCleanService.Interface.EventHandlers
{

    public class CleanReservationEventHandler : IEventHandler<CreateReservationEvent>
    {
        private readonly IMediator _mediator;
        private readonly ILogger<CleanReservationEventHandler> _logger;

        public CleanReservationEventHandler(IMediator mediator, ILogger<CleanReservationEventHandler> logger)
        {
            _mediator = mediator;
            _logger = logger;
        }

        public async Task Handle(CreateReservationEvent @event)
        {
            _logger.LogInformation($"Handled CreateReservationEvent for {@event.StartDate} -> {@event.EndDate} : {@event.Room} room");
            int cleanerId = @event.Room / 20;


            await _mediator.Send(new CreateCleaningScheduleCommand(DateOnly.FromDateTime(@event.StartDate), DateOnly.FromDateTime(@event.EndDate), @event.Room,cleanerId, @event.NumberOfPeople));

            return;
        }
    }
}
