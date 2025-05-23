(define (domain ball-moving-robot)

(:requirements :strips :typing :equality :fluents :action-costs)
(:functions (total-cost))
(:types robot room ball arm)

(:predicates
    (at ?r - robot ?rm - room)
    (inroom ?b - ball ?rm - room)
    (holding ?a - arm ?b - ball)
    (arm-empty ?a - arm)
)

(
    :action move
    :parameters (?r - robot ?from - room ?to - room)
    :precondition (at ?r ?from)
    :effect (and (not (at ?r ?from)) (at ?r ?to)
        (increase (total-cost) 5))
    
)

(
    :action pick-up
    :parameters (?r - robot ?a - arm ?b - ball ?rm - room)
    :precondition (and (at ?r ?rm) (inroom ?b ?rm) (arm-empty ?a))
    :effect (and 
        (holding ?a ?b) 
        (not (arm-empty ?a)) 
        (not (inroom ?b ?rm))     
        (increase (total-cost) 1)
    ) 
)

(
    :action put-down
    :parameters (?r - robot ?a - arm ?b - ball ?rm - room)
    :precondition (and (at ?r ?rm) (holding ?a ?b))
    :effect (and 
        (inroom ?b ?rm) 
        (arm-empty ?a) 
        (not (holding ?a ?b))     
        (increase (total-cost) 1)
    )
)

(:action pick-up-two
  :parameters (?r - robot ?a1 - arm ?a2 - arm ?b1 - ball ?b2 - ball ?rm - room)
  :precondition (and
    (at ?r ?rm)
    (not (= ?a1 ?a2))
    (arm-empty ?a1)
    (arm-empty ?a2)
    (inroom ?b1 ?rm)
    (inroom ?b2 ?rm)
    (not (= ?b1 ?b2))
  )
  :effect (and
    (holding ?a1 ?b1)
    (holding ?a2 ?b2)
    (not (arm-empty ?a1))
    (not (arm-empty ?a2))
    (not (inroom ?b1 ?rm))
    (not (inroom ?b2 ?rm))
    (increase (total-cost) 2)
  )
)

)