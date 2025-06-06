(define (problem delivery-problem)
  (:domain delivery)

  (:objects
    package1 package2 package3 package4 - package

    warehouse1 warehouse2 - warehouse
    airport1 airport2 - airport
    harbor1 harbor2 - harbor

    car1 car2 car3 - car
    plane1 - plane
    ship1 - ship
  )

  (:init

    (package package1) (package package2)
    (package package3) (package package4)

    (at-vehicle car1 warehouse1)
    (at-vehicle car2 airport2)
    (at-vehicle car3 harbor2)
    (at-vehicle plane1 airport1)
    (at-vehicle ship1 harbor1)

    (at package1 warehouse1)
    (at package2 warehouse1)
    (at package3 warehouse1)
    (at package4 warehouse1)


    (allowed-move car1 warehouse1 airport1)
    (allowed-move car1 airport1 warehouse1)

    (allowed-move plane1 airport1 airport2)
    (allowed-move plane1 airport2 airport1)

    (allowed-move car2 airport2 harbor1)
    (allowed-move car2 harbor1 airport2)

    (allowed-move ship1 harbor1 harbor2)
    (allowed-move ship1 harbor2 harbor1)

    (allowed-move car3 harbor2 warehouse2)
    (allowed-move car3 warehouse2 harbor2)

    (= (capacity car1) 2)
    (= (capacity car2) 1)
    (= (capacity car3) 2)
    (= (capacity plane1) 4)
    (= (capacity ship1) 3)

    (= (load car1) 0)
    (= (load car2) 0)
    (= (load car3) 0)
    (= (load plane1) 0)
    (= (load ship1) 0)

    (= (total-cost) 0)

    (= (move-cost car1) 2)
    (= (move-cost car2) 2)
    (= (move-cost car3) 2)
    (= (move-cost plane1) 5)
    (= (move-cost ship1) 4)


  )

  (:goal
    (and
      (at package1 warehouse2)
      (at package2 warehouse2)
      (at package3 warehouse2)
      (at package4 warehouse2)
    )
  )
  (:metric minimize (total-cost))

)
