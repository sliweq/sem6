using MediatR;
using MicroReservation.Domain.DTO;
using Microsoft.AspNetCore.Mvc;
using MicroReservation.Domain.Queries;
using MicroReservation.Domain.Commands;


namespace MicroReservation.API.Controllers
{


    public class ReservationController : ControllerBase
    {
        private readonly ILogger<ReservationController> _logger;
        private readonly IMediator _mediator;

        public ReservationController(IMediator mediator, ILogger<ReservationController> logger)
        {
            _logger = logger;
            _mediator = mediator;
        }

        [HttpPost("Reservation")]
        public async Task<IActionResult> Post([FromBody] CreateReservationDTO dto)
        {
            _logger.LogInformation($"{nameof(Post)} Create Reservation (controller) for {dto.UserName} {dto.StartDate} {dto.EndDate} for {dto.NumberOfPeople} people");
            if (dto.EndDate <= dto.StartDate) { 
                var tmp = dto.StartDate;
                dto.StartDate = dto.EndDate;
                dto.EndDate = tmp;
            }

            if (DateOnly.FromDateTime(dto.StartDate) == DateOnly.FromDateTime(dto.EndDate)) {
                _logger.LogWarning($"{nameof(Post)} Between dates must be at least 1 day difference");

                return BadRequest(new { Error = "Between dates must be at least 1 day difference" });

            }

            if (dto.NumberOfPeople > 5 || dto.NumberOfPeople <= 0) {
                _logger.LogWarning($" {nameof(Post)} Max amount of people is 5 and lowest is 1");

                return BadRequest(new { Error = "Max amount of people is 5 and lowest is 1" });

            }
            var response = await _mediator.Send(new GetEmptyRoomsQuery(dto.StartDate, dto.EndDate, dto.NumberOfPeople));
            if (response.Count == 0)
            {
                _logger.LogWarning($" {nameof(Post)} No empty rooms");

                return BadRequest(new { Error = "No empty rooms" });
            }
            var room = response[0];

            await _mediator.Send(new CreateReservationCommand(dto.UserName,dto.StartDate,dto.EndDate,dto.NumberOfPeople,room.Id));
            return Ok();
        }
    }
}
