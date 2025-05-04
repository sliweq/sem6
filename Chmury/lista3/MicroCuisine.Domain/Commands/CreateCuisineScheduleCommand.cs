using Hotel.Common.Domain.Commands;
using MicroCuisine.Domain.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCuisine.Domain.Commands
{
    public class CreateCuisineScheduleCommand : Command
    {
        public DateOnly StartDate { get; set; }
        public DateOnly EndDate { get; set; }
        public int Meals { get; set; }
        public List<CuisineScheduleDTO> Lista { get; set; }

        public CreateCuisineScheduleCommand(DateOnly startDate, DateOnly endDate ,int meals)
        {
            EndDate = endDate;
            StartDate = startDate;
            Meals = meals;
        }
        public CreateCuisineScheduleCommand(List<CuisineScheduleDTO> lista, int meals)
        {
            Lista = lista;
            Meals = meals;
        }
        public CreateCuisineScheduleCommand(DateOnly startDate, DateOnly endDate, List<CuisineScheduleDTO> lista, int meals)
        {
            Lista = lista;
            Meals = meals;
            EndDate = endDate;
            StartDate = startDate;
        }
    }
}
