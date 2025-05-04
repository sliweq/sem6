
using Microsoft.Extensions.Logging;
using Supabase.Postgrest.Models;

namespace Hotel.Infra.Bus
{

    public class Repository<T> where T : BaseModel, new()
    {
        private readonly SupabaseService<T> _supabaseService;
        private readonly ILogger<Repository<T>> _logger;

        public Repository(SupabaseService<T> supabaseService, ILogger<Repository<T>> logger)
        {
            _supabaseService = supabaseService;
            _logger = logger;
        }

        public async Task<IEnumerable<T>> GetAllAsync()
        {
            var client = _supabaseService.GetClient();
            var response = await client.From<T>().Get();
            return response.Models;
        }

        public async Task<T> GetByIdAsync(Guid id)
        {
            var client = _supabaseService.GetClient();
            var response = await client.From<T>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id)
                .Get();
            return response.Models.FirstOrDefault();
        }

        public async Task<IEnumerable<T>> InsertAsync(List<T> entities)
        {
            _logger.LogInformation($"InsertAsync {typeof(T)}");
            var client = _supabaseService.GetClient();
            var response = await client.From<T>().Insert(entities);
            return response.Models;
        }

        public async Task UpdateAsync(T entity)
        {
            _logger.LogInformation($"Udapte Async {typeof(T)}");
            var client = _supabaseService.GetClient();
            await client.From<T>().Update(entity);
        }

        public async Task DeleteAsync(Guid id)
        {
            var client = _supabaseService.GetClient();
            await client.From<T>()
                .Filter("id", Supabase.Postgrest.Constants.Operator.Equals, id)
                .Delete();
        }

        public Supabase.Client Query()
        {
            _logger.LogInformation($"Query {typeof(T)}");
            var client = _supabaseService.GetClient();
            return _supabaseService.GetClient();
        }
    }
}
