import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class CompilerSwingApp extends JFrame {

    private JTextArea inputArea;
    private JTextArea tacArea;
    private JTextArea bbArea;
    private JTextArea cfgArea;
    private JButton compileBtn;

    public CompilerSwingApp() {
        setTitle("Intermediate Code Generator - Case Study 2");
        setSize(900, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Setup UI
        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setBorder(BorderFactory.createTitledBorder("Source Code"));
        inputArea = new JTextArea(8, 50);
        inputArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
        inputArea.setText("if(a>b)\n    c=a+b;\nelse\n    c=a-b;");
        topPanel.add(new JScrollPane(inputArea), BorderLayout.CENTER);

        compileBtn = new JButton("Compile & Generate");
        JPanel btnPanel = new JPanel();
        btnPanel.add(compileBtn);
        topPanel.add(btnPanel, BorderLayout.SOUTH);

        add(topPanel, BorderLayout.NORTH);

        JTabbedPane tabbedPane = new JTabbedPane();
        
        tacArea = createTextArea();
        bbArea = createTextArea();
        cfgArea = createTextArea();

        tabbedPane.addTab("Three Address Code", new JScrollPane(tacArea));
        tabbedPane.addTab("Basic Blocks", new JScrollPane(bbArea));
        tabbedPane.addTab("Control Flow Graph", new JScrollPane(cfgArea));

        add(tabbedPane, BorderLayout.CENTER);

        compileBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                compile();
            }
        });
    }

    private JTextArea createTextArea() {
        JTextArea area = new JTextArea();
        area.setFont(new Font("Monospaced", Font.PLAIN, 14));
        area.setEditable(false);
        return area;
    }

    private void compile() {
        String input = inputArea.getText().trim();
        // A specific parsing approach mimicking the requested TAC output.
        // For demonstration, we will handle the exact structure requested:
        // if(...) ... else ...
        
        if(input.startsWith("if(")) {
            int endCond = input.indexOf(")");
            String cond = input.substring(3, endCond).trim();
            
            int elseIdx = input.indexOf("else");
            String thenPart = input.substring(endCond + 1, elseIdx).replace(";", "").trim();
            String elsePart = input.substring(elseIdx + 4).replace(";", "").trim();

            List<String> tac = new ArrayList<>();
            tac.add("t1=" + cond);
            tac.add("ifFalse t1 goto L1");
            tac.add(thenPart);
            tac.add("goto L2");
            tac.add("L1:");
            tac.add(elsePart);
            tac.add("L2:");

            StringBuilder tacSb = new StringBuilder();
            for(String s : tac) tacSb.append(s).append("\n");
            tacArea.setText(tacSb.toString());

            // Basic Blocks
            StringBuilder bbSb = new StringBuilder();
            bbSb.append("Block B1 (Leader: t1=").append(cond).append(")\n");
            bbSb.append("  t1=").append(cond).append("\n");
            bbSb.append("  ifFalse t1 goto L1\n\n");
            
            bbSb.append("Block B2 (Leader: ").append(thenPart).append(")\n");
            bbSb.append("  ").append(thenPart).append("\n");
            bbSb.append("  goto L2\n\n");

            bbSb.append("Block B3 (Leader: L1:)\n");
            bbSb.append("  L1:\n");
            bbSb.append("  ").append(elsePart).append("\n\n");

            bbSb.append("Block B4 (Leader: L2:)\n");
            bbSb.append("  L2:\n");
            
            bbArea.setText(bbSb.toString());

            // CFG
            StringBuilder cfgSb = new StringBuilder();
            cfgSb.append("Nodes: {B1, B2, B3, B4}\n\n");
            cfgSb.append("Edges:\n");
            cfgSb.append("B1 -> B2 (True Path)\n");
            cfgSb.append("B1 -> B3 (False Path, goto L1)\n");
            cfgSb.append("B2 -> B4 (goto L2)\n");
            cfgSb.append("B3 -> B4 (Fall-through)\n\n");
            
            cfgSb.append("Adjacency List:\n");
            cfgSb.append("B1: [B2, B3]\n");
            cfgSb.append("B2: [B4]\n");
            cfgSb.append("B3: [B4]\n");
            cfgSb.append("B4: []\n");

            cfgArea.setText(cfgSb.toString());
        } else {
            tacArea.setText("Please enter the specific if-else format.");
            bbArea.setText("");
            cfgArea.setText("");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new CompilerSwingApp().setVisible(true);
        });
    }
}
