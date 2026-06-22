import javax.swing.*;
import java.awt.event.*;

public class CompilerFrontEnd extends JFrame {
    private JTextField expressionField;
    private JTextField outputDisplay;
    private JButton computeBtn;

    public CompilerFrontEnd() {
        setTitle("Expression Evaluator");
        setSize(400, 250);
        setLayout(null);

        JLabel lblInput = new JLabel("Enter Expression:");
        lblInput.setBounds(30, 60, 150, 20);
        add(lblInput);

        expressionField = new JTextField();
        expressionField.setBounds(30, 80, 340, 30);
        add(expressionField);

        computeBtn = new JButton("ComputeResult");
        computeBtn.setBounds(150, 130, 150, 30);
        add(computeBtn);

        JLabel lblOutput = new JLabel("Result:");
        lblOutput.setBounds(30, 180, 150, 20);
        add(lblOutput);

        outputDisplay = new JTextField();
        outputDisplay.setBounds(80, 175, 290, 30);
        outputDisplay.setEditable(false);
        add(outputDisplay);

        computeBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    double val = computeResult(expressionField.getText());
                    outputDisplay.setText(String.valueOf(val));
                } catch(Exception ex) {
                    outputDisplay.setText("Syntax Error");
                }
            }
        });
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    
    // Recursive Descent Parser Logic
    private double computeResult(String exp) {
        return new Object() {
            int pos = -1, ch;
            void nextChar() { ch = (++pos < exp.length()) ? exp.charAt(pos) : -1; }
            boolean eat(int charToEat) {
                while (ch == ' ') nextChar();
                if (ch == charToEat) { nextChar(); return true; }
                return false;
            }
            double parse() {
                nextChar();
                double x = parseExpression();
                if (pos < exp.length()) throw new RuntimeException("Unexpected: " + (char)ch);
                return x;
            }
            double parseExpression() {
                double x = parseTerm();
                for (;;) {
                    if      (eat('+')) x += parseTerm();
                    else if (eat('-')) x -= parseTerm();
                    else return x;
                }
            }
            double parseTerm() {
                double x = parseFactor();
                for (;;) {
                    if      (eat('*')) x *= parseFactor();
                    else if (eat('/')) x /= parseFactor();
                    else return x;
                }
            }
            double parseFactor() {
                if (eat('+')) return parseFactor();
                if (eat('-')) return -parseFactor();
                double x;
                int startPos = this.pos;
                if (eat('(')) {
                    x = parseExpression();
                    eat(')');
                } else if ((ch >= '0' && ch <= '9') || ch == '.') {
                    while ((ch >= '0' && ch <= '9') || ch == '.') nextChar();
                    x = Double.parseDouble(exp.substring(startPos, this.pos));
                } else {
                    throw new RuntimeException("Unexpected: " + (char)ch);
                }
                return x;
            }
        }.parse();
    }
    public static void main(String[] args) {
        new CompilerFrontEnd().setVisible(true);
    }
}
