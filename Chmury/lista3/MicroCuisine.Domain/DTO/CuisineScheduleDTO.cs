using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCuisine.Domain.DTO
{
    public class CuisineScheduleDTO
    {
        public Guid id;
        public int meals;
        public DateOnly date;
        public CuisineScheduleDTO(Guid id, int meals, DateOnly date)
        {
            this.id = id;
            this.meals = meals;
            this.date = date;
        }
    }
}
