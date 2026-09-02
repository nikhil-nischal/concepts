package com.conceptcoding.interviewquestions.elevator;

import com.conceptcoding.interviewquestions.elevator.enums.ElevatorDirection;

import java.util.List;

public class ExternalDispatcher {

    ElevatorScheduler scheduler;

    public ExternalDispatcher(ElevatorScheduler scheduler) {
        this.scheduler = scheduler;
    }

    public void submitExternalRequest(int floor, ElevatorDirection direction) {

        ElevatorController controller =
                scheduler.assignElevator(floor, direction);
        controller.submitRequest(floor);
    }

}
