using MediatR;
using MicroReservation.Domain.DTO;
using Microsoft.EntityFrameworkCore;
using System;
using System.Data;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.Queries
{
    public class GetReservationQuery : IRequest<ReservationDTO>
    {
        public Guid Id { get; protected set; }

        public GetReservationQuery(Guid id)
        {
            Id = id;
        }
    }
}
