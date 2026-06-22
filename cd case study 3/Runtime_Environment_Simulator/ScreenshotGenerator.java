import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.util.Stack;
import java.util.ArrayList;

public class ScreenshotGenerator extends JFrame {
    private JTable stackTable;
    private JTable heapTable;
    private DefaultTableModel executionStackModel;
    private DefaultTableModel dynamicMemoryModel;

    private Stack<String> executionStack;
    private ArrayList<String[]> dynamicMemory;

    public ScreenshotGenerator() {
        setTitle("Runtime Environment Simulator - Case Study 3");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        executionStack = new Stack<>();
        dynamicMemory = new ArrayList<>();

        // Create Execution Stack Panel
        JPanel stackPanel = new JPanel(new BorderLayout());
        stackPanel.setBorder(BorderFactory.createTitledBorder("Execution Stack (Activation Records)"));
        executionStackModel = new DefaultTableModel(new Object[]{"Address", "Function Frame", "State"}, 0);
        stackTable = new JTable(executionStackModel);
        stackTable.setFont(new Font("Monospaced", Font.PLAIN, 14));
        stackTable.setRowHeight(30);
        stackPanel.add(new JScrollPane(stackTable), BorderLayout.CENTER);

        // Create Dynamic Memory Panel
        JPanel heapPanel = new JPanel(new BorderLayout());
        heapPanel.setBorder(BorderFactory.createTitledBorder("Dynamic Memory (Heap Allocation)"));
        dynamicMemoryModel = new DefaultTableModel(new Object[]{"Object ID", "Type", "Status"}, 0);
        heapTable = new JTable(dynamicMemoryModel);
        heapTable.setFont(new Font("Monospaced", Font.PLAIN, 14));
        heapTable.setRowHeight(30);
        heapPanel.add(new JScrollPane(heapTable), BorderLayout.CENTER);

        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, stackPanel, heapPanel);
        splitPane.setDividerLocation(400);
        add(splitPane, BorderLayout.CENTER);

        // Top info panel
        JPanel topPanel = new JPanel();
        topPanel.setBackground(new Color(230, 240, 255));
        JLabel titleLabel = new JLabel("Runtime Memory Organization Viewer");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        topPanel.add(titleLabel);
        add(topPanel, BorderLayout.NORTH);
    }

    public void refreshStackView() {
        executionStackModel.setRowCount(0);
        int address = 0x7FFF;
        for (int i = executionStack.size() - 1; i >= 0; i--) {
            executionStackModel.addRow(new Object[]{String.format("0x%04X", address), executionStack.get(i), "ACTIVE"});
            address -= 0x0040;
        }
    }

    public void refreshHeapView() {
        dynamicMemoryModel.setRowCount(0);
        for (String[] obj : dynamicMemory) {
            dynamicMemoryModel.addRow(obj);
        }
    }

    public void captureScreenshot(String filename) {
        try {
            Robot robot = new Robot();
            Rectangle bounds = this.getBounds();
            BufferedImage image = robot.createScreenCapture(bounds);
            ImageIO.write(image, "png", new File(filename));
            System.out.println("Saved screenshot: " + filename);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ScreenshotGenerator gui = new ScreenshotGenerator();
        gui.setVisible(true);

        // Scenario 1: Function Calls
        gui.executionStack.push("main()");
        gui.executionStack.push("display()");
        gui.executionStack.push("calculate()");
        gui.refreshStackView();
        Thread.sleep(1000);
        gui.captureScreenshot("scenario1.png");

        // Scenario 2: Heap Allocation
        gui.dynamicMemory.add(new String[]{"OBJ_101", "Customer Object", "Reachable"});
        gui.dynamicMemory.add(new String[]{"OBJ_102", "Student Object", "Reachable"});
        gui.dynamicMemory.add(new String[]{"OBJ_103", "Employee Object", "Reachable"});
        gui.refreshHeapView();
        Thread.sleep(1000);
        gui.captureScreenshot("scenario2.png");

        // Scenario 3: Garbage Collection
        gui.dynamicMemory.set(1, new String[]{"OBJ_102", "Student Object", "Unreachable (Garbage)"});
        gui.refreshHeapView();
        Thread.sleep(1000);
        
        gui.dynamicMemory.remove(1); // GC removes the object
        gui.dynamicMemoryModel.setRowCount(0);
        for (String[] obj : gui.dynamicMemory) {
            gui.dynamicMemoryModel.addRow(obj);
        }
        gui.dynamicMemoryModel.addRow(new Object[]{"---", "Memory Reclaimed", "---"});
        
        Thread.sleep(1000);
        gui.captureScreenshot("scenario3.png");

        System.exit(0);
    }
}
