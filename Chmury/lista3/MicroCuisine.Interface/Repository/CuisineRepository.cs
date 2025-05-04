using Hotel.Infra.Bus;
using MicroCuisine.Domain.DbEntities;
using Microsoft.Extensions.Logging;

namespace MicroCuisine.Interface.Repository
{
    public class CuisineRepository : Repository<CuisineSchedule>

    {
        public CuisineRepository(SupabaseService<CuisineSchedule> supabaseService, ILogger<Repository<CuisineSchedule>> logger) : base(supabaseService, logger)
        {
        }
    }
}
