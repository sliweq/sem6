using MediatR;
using MicroLaundry.Domain.DTO;

namespace MicroLaundry.Domain.Queries
{
    public class GetLaundryQuery : IRequest<List<LaundryDTO>>
    {
        public DateOnly StartDate { get; protected set; }
        public DateOnly EndDate { get; protected set; }

        public GetLaundryQuery(DateOnly startDate, DateOnly endDate)
        {
            StartDate = startDate;
            EndDate = endDate;
        }
    }
}
