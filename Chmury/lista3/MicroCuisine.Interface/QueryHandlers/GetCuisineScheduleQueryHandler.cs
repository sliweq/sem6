using MediatR;
using MicroCuisine.Domain.DbEntities;
using MicroCuisine.Domain.DTO;
using MicroCuisine.Domain.Queries;
using MicroCuisine.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroCuisine.Interface.QueryHandlers
{
    public class GetCuisineScheduleQueryHandler : IRequestHandler<GetCuisineScheduleQuery, List<CuisineScheduleDTO>>
    {
        private readonly CuisineRepository _cuisineRepository;
        private readonly ILogger<GetCuisineScheduleQueryHandler> _logger;

        public GetCuisineScheduleQueryHandler(CuisineRepository cuisineRepository, ILogger<GetCuisineScheduleQueryHandler> logger)
        {
            _cuisineRepository = cuisineRepository;
            _logger = logger;
        }

        public async Task<List<CuisineScheduleDTO>> Handle(GetCuisineScheduleQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested GetCuisineScheduleQuery for {request.StartDate} {request.EndDate}");

            var client =  _cuisineRepository.Query();

            var startDateString = request.StartDate.ToString("yyyy-MM-dd");
            var endDateString = request.EndDate.ToString("yyyy-MM-dd");

            var hotelBoysResponse = await client
                .From<CuisineSchedule>()
                .Filter("date", Supabase.Postgrest.Constants.Operator.GreaterThanOrEqual, startDateString)
                .Filter("date", Supabase.Postgrest.Constants.Operator.LessThanOrEqual, endDateString)
                .Get();
   
            var tmp = hotelBoysResponse.Models
                .Select(room => new CuisineScheduleDTO(room.id,room.meals,room.date)).ToList();

            return tmp;
        }
    }
}
