package org.cbritton.aoc;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public abstract class AbstractSolver {

    private Object data = null;

    public abstract Object initData(String data_file_path);

    public abstract Object solvePart1(Object data);

    public abstract Object solvePart2(Object data);

    public abstract int getDay();

    public Object part1(String dataFilePath) {
        Timer timer = new Timer();
        Object answer = this.solvePart1(this.initData(dataFilePath));
        timer.stop();

        this.printInfo("Part 1", timer, answer);

        return answer;
    }

    public Object part2(String dataFilePath) {
        Timer timer = new Timer();
        Object answer = this.solvePart2(this.initData(dataFilePath));
        timer.stop();

        this.printInfo("Part 2", timer, answer);

        return answer;
    }

    public void run() {

        int day = this.getDay();
        String resourcesDirPath = System.getenv("RESOURCES_DIR_PATH");
        String dataFilePath = String.format("%s%sday%02d.data", resourcesDirPath, File.separator, day);

        this.part1(dataFilePath);
        this.part2(dataFilePath);
        return;
    }

    protected void printInfo(String part, Timer timer, Object answer) {
        System.out.printf("%s\n    Elapsed Time: %s\n          Answer: %s%n", part, timer.elapsedTime(), answer);
    }

    protected Object getData(int day, String dataFilePath) {

        String path;
        if (null != dataFilePath) {
            path = dataFilePath;
        } else {
            String resourcesDirPath = System.getenv("RESOURCES_DIR_PATH");
            path = String.format("%s%sday%02d.data", resourcesDirPath, File.separator, day);
        }

        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            String line;
            while (null != (line = reader.readLine())) {
                lines.add(line);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return lines;
    }
}
