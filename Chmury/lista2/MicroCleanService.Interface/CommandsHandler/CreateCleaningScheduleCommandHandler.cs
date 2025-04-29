using Hotel.Common.Domain.Bus;
using MediatR;
using MicroCleanService.Domain.Commands;
using MicroCleanService.Domain.DbEntities;
using MicroCleanService.Domain.Events;
using MicroCleanService.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroCleanService.Interface.CommandsHandler
{
    public class CreateCleaningScheduleCommandHandler : IRequestHandler<CreateCleaningScheduleCommand, bool>
    {
        private readonly IEventBus _eventBus;
        private readonly CleaningSchedulesRepository _cleaningSchedulesRepository;
        private readonly ILogger<CreateCleaningScheduleCommandHandler> _logger;
        public CreateCleaningScheduleCommandHandler(CleaningSchedulesRepository cleaningSchedulesRepository, IEventBus eventBus, ILogger<CreateCleaningScheduleCommandHandler> logger)
        {
            _logger = logger; 
            _cleaningSchedulesRepository = cleaningSchedulesRepository;
            _eventBus = eventBus;
        }
        public async Task<bool> Handle(CreateCleaningScheduleCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested CreateCleaningScheduleCommand for {request.StartDate}->{request.EndDate} room: {request.Room} cleaner: {request.Cleaner}");
            var cleaningSchedules = new List<CleaningSchedule>();
            for (var date = request.StartDate.AddDays(1); date <= request.EndDate; date = date.AddDays(1)) { 
                cleaningSchedules.Add(new CleaningSchedule(
                    date,
                    request.Room,
                    request.Cleaner,
                    request.PeopleInRoom
                ));
            }

            await _cleaningSchedulesRepository.InsertAsync(cleaningSchedules);


            await _eventBus.Publish(new CreateCleaningEvent(
                request.Room,
                request.PeopleInRoom,
                request.StartDate.AddDays(1),
                request.EndDate,
                request.Cleaner
            ));

            return true;

        }
    }
}
