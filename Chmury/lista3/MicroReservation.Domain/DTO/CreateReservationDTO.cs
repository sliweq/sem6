﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.DTO
{
    public class CreateReservationDTO
    {
        public string UserName { get; set; }

        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int NumberOfPeople { get; set; }

    }
}
