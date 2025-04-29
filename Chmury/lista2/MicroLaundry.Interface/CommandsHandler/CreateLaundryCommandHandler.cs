using Hotel.Common.Domain.Bus;
using MediatR;
using MicroLaundry.Domain.Commands;
using MicroLaundry.Domain.DbEntities;
using MicroLaundry.Domain.DTO;
using MicroLaundry.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroLaundry.Interface.CommandsHandler
{
    public class CreateLaundryCommandHandler : IRequestHandler<CreateLaundryCommand, bool>
    {
        private readonly IEventBus _eventBus;
        private readonly LaundryRepository _laundryRepository;
        private readonly ILogger<CreateLaundryCommandHandler> _logger;
        public CreateLaundryCommandHandler(LaundryRepository laundryRepository, IEventBus eventBus, ILogger<CreateLaundryCommandHandler> logger)
        {
            _laundryRepository = laundryRepository;
            _eventBus = eventBus;
            _logger = logger;
        }
        public async Task<bool> Handle(CreateLaundryCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested CreateLaundryCommand for {request.StartDate} -> {request.EndDate} : {request.PeopleInRoom} people");

            var startDate = request.StartDate;
            var endDate = request.EndDate;
            var additionalSheets = request.PeopleInRoom;

            var updatedList = new List<LaundryDTO>(request.Lista);

            for (var date = startDate; date <= endDate; date = date.AddDays(1))
            {
                var existingEntry = updatedList.FirstOrDefault(x => x.Date == date);

                if (existingEntry != null)
                {
                    existingEntry.SheetCount += additionalSheets;
                }
                else
                {
                    updatedList.Add(new LaundryDTO(Guid.NewGuid(), date, additionalSheets));
                }
            }
            var newLaundryList = new List<Laundry>();
            for (int i = 0; i < updatedList.Count; i++)
            {
                var existingEntry = request.Lista.FirstOrDefault(x => x.Date == updatedList[i].Date);

                if (existingEntry != null)
                {

                    await _laundryRepository.UpdateAsync(new Laundry(updatedList[i].Id, updatedList[i].Date, updatedList[i].SheetCount));
                }
                else
                {
                    newLaundryList.Add(new Laundry(updatedList[i].Date, updatedList[i].SheetCount));
                }
            }
            if (newLaundryList.Count != 0) { 
                await _laundryRepository.InsertAsync(newLaundryList);
            }

            return true;

        }
    }
}
