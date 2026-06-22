import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;

public class ScreenshotGenerator {

    public static void saveComponentAsImage(Component comp, String fileName) throws Exception {
        BufferedImage img = new BufferedImage(comp.getWidth(), comp.getHeight(), BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = img.createGraphics();
        comp.paint(g2d);
        g2d.dispose();
        ImageIO.write(img, "png", new File(fileName));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                CompilerSwingApp app = new CompilerSwingApp();
                app.pack();
                app.setSize(900, 700);
                app.setVisible(true);

                // Trigger compile
                app.getContentPane().getComponent(0).dispatchEvent(
                    new java.awt.event.ActionEvent(app, java.awt.event.ActionEvent.ACTION_PERFORMED, "")
                );

                JTabbedPane tabs = (JTabbedPane) app.getContentPane().getComponent(1);

                // Tab 0
                tabs.setSelectedIndex(0);
                app.getContentPane().validate();
                app.getContentPane().repaint();
                saveComponentAsImage(app.getContentPane(), "tac_output.png");

                // Tab 1
                tabs.setSelectedIndex(1);
                app.getContentPane().validate();
                app.getContentPane().repaint();
                saveComponentAsImage(app.getContentPane(), "bb_output.png");

                // Tab 2
                tabs.setSelectedIndex(2);
                app.getContentPane().validate();
                app.getContentPane().repaint();
                saveComponentAsImage(app.getContentPane(), "cfg_output.png");

                System.out.println("Screenshots generated successfully using paint().");
                System.exit(0);

            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
}
