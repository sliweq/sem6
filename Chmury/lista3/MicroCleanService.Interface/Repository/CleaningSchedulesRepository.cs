using Hotel.Infra.Bus;
using MicroCleanService.Domain.DbEntities;
using Microsoft.Extensions.Logging;


namespace MicroCleanService.Interface.Repository
{
    public class CleaningSchedulesRepository : Repository<CleaningSchedule>
    {
        public CleaningSchedulesRepository(SupabaseService<CleaningSchedule> supabaseService, ILogger<Repository<CleaningSchedule>> logger) : base(supabaseService,logger)
        {
        }
    }
}
