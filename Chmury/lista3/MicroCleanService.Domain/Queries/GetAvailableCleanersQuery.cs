using MediatR;
using MicroCleanService.Domain.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCleanService.Domain.Queries
{
    public class GetAvailableCleanersQuery : IRequest<List<CleanerDTO>>
    {
        public DateOnly Date { get; protected set; }
        public int Room { get; protected set; }

        public GetAvailableCleanersQuery(DateOnly date, int room)
        {
            Date = date;
            Room = room;
        }
    }
}
