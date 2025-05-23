using Hotel.Common.Domain.Bus;
using MediatR;
using MicroCuisine.Domain.Commands;
using MicroCuisine.Domain.DTO;
using MicroCuisine.Domain.Events;


using MicroCuisine.Domain.Queries;
using MicroCuisine.Interface.CommandsHandler;
using Microsoft.Extensions.Logging;

namespace MicroCuisine.Interface.EventHandlers
{
    public class CuisineReservationEventHandler : IEventHandler<CreateReservationEvent>
    {
        private readonly IMediator _mediator;
        private readonly ILogger<CuisineReservationEventHandler> _logger;

        public CuisineReservationEventHandler(IMediator mediator, ILogger<CuisineReservationEventHandler> logger)
        {
            _mediator = mediator;
            _logger = logger;
        }
        public async Task Handle(CreateReservationEvent @event)
        {
            _logger.LogInformation($"Handled CreateReservationEvent for {@event.StartDate} -> {@event.EndDate} : {@event.Room} room");
            var response = await _mediator.Send(new GetCuisineScheduleQuery(DateOnly.FromDateTime(@event.StartDate), DateOnly.FromDateTime(@event.EndDate),@event.NumberOfPeople));

            if (response is null)
            {
                return;
            }
            
            await _mediator.Send(new CreateCuisineScheduleCommand(DateOnly.FromDateTime(@event.StartDate), DateOnly.FromDateTime(@event.EndDate), response,@event.NumberOfPeople));

            return;
        }
    }
}
