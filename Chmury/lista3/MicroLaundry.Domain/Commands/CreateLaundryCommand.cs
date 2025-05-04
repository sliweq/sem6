using Hotel.Common.Domain.Commands;
using MicroLaundry.Domain.DTO;

namespace MicroLaundry.Domain.Commands
{
    public class CreateLaundryCommand : Command
    {
        public int PeopleInRoom { get; set; }
        public List<LaundryDTO> Lista { get; set; }
        public DateOnly StartDate { get; set; }

        public DateOnly EndDate { get; set; }


        public CreateLaundryCommand(List<LaundryDTO> lista, int peopleInRoom, DateOnly startDate, DateOnly endDate)
        {
            Lista = lista;
            PeopleInRoom = peopleInRoom;
            StartDate = startDate;
            EndDate = endDate;
        }
    }
}
