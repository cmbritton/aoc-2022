package org.cbritton.aoc.y2022;

import org.cbritton.aoc.AbstractSolver;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day15 extends AbstractSolver {

    public int row = 2000000;

    public int max_xy = 4000000;

    public Day15() {
    }

    @Override
    public Object initData(String dataFilePath) {
        List<String> lines = (List<String>) this.getData(this.getDay(), dataFilePath);

        String pattern = "Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)";
        Pattern p = Pattern.compile(pattern);

        List<Sensor> sensors = new ArrayList<>();
        for (String line : lines) {
            Matcher m = p.matcher(line);
            if (m.matches()) {
                Point p1 = new Point(Integer.parseInt(m.group(3)), Integer.parseInt(m.group(4)));
                Beacon beacon = new Beacon(p1);
                Point p2 = new Point(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)));
                Sensor sensor = new Sensor(p2);
                sensor.beacon = beacon;
                sensors.add(sensor);
            }
        }

        return sensors;
    }

    private boolean currentContainsNext(Interval currentInterval, Interval nextInterval) {
        return currentInterval.start <= nextInterval.start && currentInterval.end >= nextInterval.end;
    }

    private boolean nextContainsCurrent(Interval currentInterval, Interval nextInterval) {
        return nextInterval.start <= currentInterval.start && nextInterval.end >= currentInterval.end;
    }

    private boolean nextExtendsCurrent(Interval currentInterval, Interval nextInterval) {
        return nextInterval.start <= currentInterval.end && currentInterval.end <= nextInterval.end;
    }

    @Override
    public Object solvePart1(Object data) {
        List<Sensor> sensors = (List<Sensor>) data;
        List<Interval> excludedXIntervals = new ArrayList<>();
        for (Sensor sensor : sensors) {
            Interval interval = sensor.excludedXInterval(this.row);
            if (null != interval) {
                excludedXIntervals.add(interval);
            }
        }
        List<Interval> collapsedIntervals = new ArrayList<>();
        Collections.sort(excludedXIntervals);
        Interval currentInterval = excludedXIntervals.get(0);
        for (Interval nextInterval : excludedXIntervals.subList(1, excludedXIntervals.size())) {
            if (this.currentContainsNext(currentInterval, nextInterval)) {
                continue;
            } else if (this.nextContainsCurrent(currentInterval, nextInterval)) {
                currentInterval = nextInterval;
                continue;
            } else if (this.nextExtendsCurrent(currentInterval, nextInterval)) {
                currentInterval.end = nextInterval.end;
            } else {
                collapsedIntervals.add(currentInterval);
                currentInterval = nextInterval;
            }
        }
        collapsedIntervals.add(currentInterval);
        return collapsedIntervals.stream().reduce(0, (a, b) -> a + (b.end - b.start), Integer::sum);
    }

    @Override
    public Object solvePart2(Object data) {
        List<Sensor> sensors = (List<Sensor>) data;
        for (int y = 0; y <= this.max_xy; ++y) {
            System.out.printf("y=%d\t%d%n", y, System.currentTimeMillis());
            for (int x = 0; x <= this.max_xy; ++x) {
                Point p = new Point(x, y);
                if (sensors.stream().noneMatch(a -> a.isInExclusionZone(p))) {
                    return (p.x * 4000000) + p.y;
                }
            }
        }
        return 0;
    }

    @Override
    public int getDay() {
        return Integer.parseInt(getClass().getSimpleName().substring(3));
    }

    public static void main(String[] argv) {
        Day15 solver = new Day15();
        solver.run();
    }


    private static class Interval implements Comparable<Interval> {

        private int start = 0;
        private int end = 0;

        public Interval(int start, int end) {
            this.start = start;
            this.end = end;
        }

        @Override
        public int compareTo(Interval o) {

            if (this.start < o.start) {
                return -1;
            } else if (this.start > o.start) {
                return 1;
            } else {
                return Integer.compare(this.end, o.end);
            }
        }
    }


    private static class Point {

        private int x = 0;
        private int y = 0;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public String toString() {
            return String.format("Point: x: %d, y: %d", this.x, this.y);
        }
    }


    private static class Beacon {

        private Point location = null;

        public Beacon(Point location) {
            this.location = location;
        }

        @Override
        public String toString() {
            return String.format("Beacon: location: %s", this.location);
        }
    }


    private static class Sensor {

        private Point location = null;
        private Beacon beacon = null;

        public Sensor(Point location) {
            this.location = location;
        }

        @Override
        public String toString() {
            return String.format("Sensor: location: %s, beacon: %s", this.location, this.beacon);
        }

        private int beaconDistance() {
            return this.taxiDistance(this.beacon.location);
        }

        private int taxiDistance(Point p) {
            return Math.abs(this.location.x - p.x) + Math.abs(this.location.y - p.y);
        }

        private Interval excludedXInterval(int y) {
            if ((this.beaconDistance() - Math.abs(y - this.location.y)) < 0) {
                return null;
            }
            int x1 = this.location.x - (this.beaconDistance() - Math.abs(y - this.location.y));
            int x2 = this.location.x + (this.beaconDistance() - Math.abs(y - this.location.y));
            return new Interval(Math.min(x1, x2), Math.max(x1, x2));
        }

        private boolean isInExclusionZone(Point p) {
            return this.taxiDistance(p) <= this.beaconDistance();
        }
    }
}
