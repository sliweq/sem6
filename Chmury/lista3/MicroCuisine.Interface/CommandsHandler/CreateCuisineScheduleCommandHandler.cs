using Hotel.Common.Domain.Bus;
using MediatR;
using MicroCuisine.Domain.Commands;
using MicroCuisine.Domain.DbEntities;
using MicroCuisine.Domain.DTO;
using MicroCuisine.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroCuisine.Interface.CommandsHandler
{
    public class CreateCuisineScheduleCommandHandler : IRequestHandler<CreateCuisineScheduleCommand, bool>
    {
        private readonly IEventBus _eventBus;
        private readonly CuisineRepository _cuisineRepository;
        private readonly ILogger<CreateCuisineScheduleCommandHandler> _logger;

        public CreateCuisineScheduleCommandHandler(CuisineRepository cuisineRepository, IEventBus eventBus, ILogger<CreateCuisineScheduleCommandHandler> logger)
        {
            _cuisineRepository = cuisineRepository;
            _logger = logger;
            _eventBus = eventBus;
        }

        public async Task<bool> Handle(CreateCuisineScheduleCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested CreateCuisineScheduleCommand for {request.StartDate}->{request.EndDate} meals: {request.Meals}");

            var startDate = request.StartDate;
            var endDate = request.EndDate;
            var additionalMeals = request.Meals;

            var updatedList = new List<CuisineScheduleDTO>(request.Lista);

            for (var date = startDate; date <= endDate; date = date.AddDays(1))
            {
                var existingEntry = updatedList.FirstOrDefault(x => x.date == date);

                if (existingEntry != null)
                {
                    existingEntry.meals += additionalMeals;
                }
                else
                {
                    updatedList.Add(new CuisineScheduleDTO(Guid.NewGuid(),additionalMeals,date));
                }
            }

            var newCuisineScheduleList = new List<CuisineSchedule>();

            for (int i = 0; i < updatedList.Count; i++)
            {
                var existingEntry = request.Lista.FirstOrDefault(x => x.date == updatedList[i].date);

                if (existingEntry != null)
                {
                    await _cuisineRepository.UpdateAsync(new CuisineSchedule(updatedList[i].id, updatedList[i].meals, updatedList[i].date));
                }
                else {
                    newCuisineScheduleList.Add(new CuisineSchedule(updatedList[i].id, updatedList[i].meals, updatedList[i].date));
                    //await _cuisineRepository.InsertAsync(new List<CuisineSchedule>() { new CuisineSchedule(updatedList[i].id, updatedList[i].meals, updatedList[i].date) });
                }
            }

            if (newCuisineScheduleList.Count != 0) {
                await _cuisineRepository.InsertAsync(newCuisineScheduleList);
            }

            return true;
        }
    }
}
