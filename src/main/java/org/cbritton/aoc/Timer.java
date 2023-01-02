package org.cbritton.aoc;

public class Timer {

    private long startTime = 0;
    private long endTime = 0;

    public Timer() {
        this.startTime = System.nanoTime();
    }

    public void stop() {
        this.endTime = System.nanoTime();
    }
    public String elapsedTime() {
        if (0 == this.endTime) {
            this.stop();
        }
        long t = this.endTime - this.startTime;
        String unit = "nanoseconds";
        if (t > 1000) {
            t /= 1000;
            unit = "microseconds";
        }
        if (t > 1000) {
            t /= 1000;
            unit = "milliseconds";
        }
        if (t > 1000) {
            t /= 1000;
            unit = "seconds";
        }
        return String.format("%2d %s", t, unit);
    }
}
