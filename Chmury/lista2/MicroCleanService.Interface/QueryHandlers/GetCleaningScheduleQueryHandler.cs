using MediatR;
using MicroCleanService.Domain.DTO;
using MicroCleanService.Domain.Queries;
using MicroCleanService.Interface.Repository;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCleanService.Interface.QueryHandlers
{
    public class GetCleaningScheduleQueryHandler : IRequestHandler<GetCleaningScheduleQuery, List<CleaningScheduleDTO>>
    {
        private readonly CleaningSchedulesRepository _cleaningSchedulesRepository;

        public GetCleaningScheduleQueryHandler(CleaningSchedulesRepository cleaningSchedulesRepository)
        {
            _cleaningSchedulesRepository = cleaningSchedulesRepository;
        }
        public async Task<List<CleaningScheduleDTO>> Handle(GetCleaningScheduleQuery request, CancellationToken cancellationToken)
        {
            return new List<CleaningScheduleDTO>();
        }
    }
}
