(define (problem cleaning-problem)
  (:domain cleaning)

  (:objects
    robo1 - robo
    room0 room1 room2 room3 - room
  )

  (:init
    (at robo1 room0)
    (clean room0)
    (dirty room1)
    (dirty room2)
    (dirty room3)

  )

  (:goal
    (and
    (clean room1)
    (clean room2)
    (clean room3)
    )
  )

)
