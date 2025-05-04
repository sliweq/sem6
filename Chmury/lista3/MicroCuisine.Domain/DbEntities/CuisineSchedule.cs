using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace MicroCuisine.Domain.DbEntities
{
    [Table("CuisineSchedules")]
    public class CuisineSchedule : BaseModel
    {
        public CuisineSchedule() { }

        public CuisineSchedule(int meals, DateOnly date) {
            id = Guid.NewGuid();
            this.meals = meals;
            this.date = date;
        }
        public CuisineSchedule(Guid id, int meals, DateOnly date)
        {
            this.id = id;
            this.meals = meals;
            this.date = date;
        }

        [PrimaryKey("id", false)]
        public Guid id { get; set; }

        [Column("meals")]
        public int meals { get; set; }
        [Column("date")]
        public DateOnly date { get; set; }
    }
}
