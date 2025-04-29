using MediatR;
using MicroCuisine.Domain.DTO;

namespace MicroCuisine.Domain.Queries
{


    public class GetCuisineScheduleQuery : IRequest<List<CuisineScheduleDTO>>
    {
        public DateOnly EndDate { get; protected set; }
        public DateOnly StartDate { get; protected set; }
        public int Meals { get; protected set; }

        public GetCuisineScheduleQuery(DateOnly startDate, DateOnly endDate, int meals)
        {
            EndDate = endDate;
            StartDate = startDate;
            Meals = meals;
        }
    }
}
