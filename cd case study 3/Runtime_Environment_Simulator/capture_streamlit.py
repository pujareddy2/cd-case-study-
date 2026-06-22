import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    print("Navigating to Streamlit app...")
    page.goto("http://localhost:8501")
    time.sleep(5) # Wait for initial load

    # Scenario 1: Function Calls (Stack Simulator)
    print("Capturing Scenario 1 (Stack Simulator)...")
    # Click on the Stack Simulator link in the sidebar
    page.click("text='Function Call Simulator'")
    time.sleep(3)
    # Click the "Run Factorial Simulation" button
    page.click("text='Run Factorial Simulation'")
    time.sleep(3)
    # Take screenshot of the main content
    page.screenshot(path="scenario1.png")
    
    # Scenario 2: Heap Allocation
    print("Capturing Scenario 2 (Heap Allocation)...")
    page.click("text='Heap Simulator'")
    time.sleep(3)
    
    # Expand "Allocate Object"
    page.click("text='Allocate Object'")
    time.sleep(1)
    
    # Actually we can't reliably type into the specific inputs without precise selectors, 
    # so we will just take a screenshot of the blank/initial Heap simulator, OR
    # we can try to fill inputs. Let's find inputs by placeholder or label if possible, 
    # but Streamlit generates dynamic IDs.
    # Streamlit inputs are usually `input` elements.
    inputs = page.query_selector_all("input[type='text']")
    if len(inputs) >= 2:
        inputs[0].fill("OBJ_101")
        inputs[1].fill("Customer Object")
        page.keyboard.press("Enter")
        page.click("text='Allocate'")
        time.sleep(2)
        
    page.screenshot(path="scenario2.png")

    # Scenario 3: GC
    print("Capturing Scenario 3 (Garbage Collection)...")
    page.click("text='Garbage Collection GC'")
    time.sleep(3)
    page.click("text='Run Mark-Sweep GC'")
    time.sleep(3)
    page.screenshot(path="scenario3.png")

    print("Screenshots captured successfully.")
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
